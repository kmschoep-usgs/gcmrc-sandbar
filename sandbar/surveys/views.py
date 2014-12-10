from collections import namedtuple

from django.conf import settings
from django.db.models import Min, Max
from django.db import connection
from django.views.generic import ListView, DetailView, View
from numpy import interp
import pandas as pd 

from common.views import SimpleWebServiceProxyView
from common.utils.geojson_utils import create_geojson_point, create_geojson_feature, create_geojson_feature_collection
from common.utils.view_utils import dictfetchall
from .models import Site, AreaVolume, AreaVolumeOutput, Sandbar
from .custom_mixins import CSVResponseMixin, JSONResponseMixin
from .db_utilities import convert_datetime_to_str, AlchemDB, get_sep_reatt_ids, determine_if_sep_reatt_exists, determine_site_survey_types
from .pandas_utils import (create_pandas_dataframe, round_series_values, datetime_to_date,
                           sum_two_columns, create_dygraphs_error_str, convert_to_float, create_sep_reatt_name)


class AreaVolumeCalcsVw(CSVResponseMixin, View):
    
    """
    New view to supersede AreaVolumeCalcsView that
    better handles parameter permutations
    """
    
    model = AreaVolumeOutput
    
    def get(self, request, *args, **kwargs):
        
        site = Site.objects.get(pk=request.GET.get('site_id'))
        ds_min = float(request.GET.get('ds_min'))
        ds_max = float(request.GET.get('ds_max'))
        parameter_type = request.GET.get('param_type')
        plot_sep = request.GET.get('sr_id', None)
        sr_exists = site.deposit_type
        calculation_types = request.GET.getlist('calc_type', None)       
        channel_total = 'Channel Total - {0} {1}'.format(site.river_mile, site.river_side)
        eddy_total = 'Eddy Total - {0} {1}'.format(site.river_mile, site.river_side)
        total_site = 'Total Site - {0} {1}'.format(site.river_mile, site.river_side)
        if plot_sep:
            sandbar_record = Sandbar.objects.get(id=plot_sep)
            sandbar_name = sandbar_record.sandbar_name
            sandbar_disp_name = create_sep_reatt_name(plot_sep)
        col_names = ('calc_date',) # keep track of the columns that are needed query
        if parameter_type == 'area2d':
            if 'eddy' in calculation_types:
                if sr_exists == 'SR':
                    if plot_sep:
                        if sandbar_name == 'sep':
                            col_names += ('eddy_s_int_area',)
                        if sandbar_name == 'reatt':
                            col_names += ('eddy_r_int_area',)
                    else:
                        col_names += ('sum_reatt_sep_area',)
                else:
                    col_names += ('eddy_int_area',)
            if 'chan' in calculation_types:
                col_names += ('chan_int_area',)              
            if 'eddy_chan_sum' in calculation_types:
                col_names += ('ts_int_area',)
        if parameter_type == 'volume':
            if 'eddy' in calculation_types:
                if sr_exists == 'SR':
                    if plot_sep:
                        if sandbar_name == 'sep':
                            col_names += ('dy_eddy_s_vol',)
                        if sandbar_name == 'reatt':
                            col_names += ('dy_eddy_r_vol',)
                    else:
                        col_names += ('dy_eddy_sum_vol',)
                else:
                    col_names += ('dy_eddy_int_vol',)
            if 'chan' in calculation_types:
                col_names += ('dy_chan_int_vol',)
            if 'eddy_chan_sum' in calculation_types:
                col_names += ('dy_ts_int_vol',)
               
        acdb = AlchemDB()
        ora = acdb.create_session()
        sql_base = 'SELECT * FROM TABLE(SB_CALCS.F_GET_AREA_VOL_TF({site_id}, {ds_min}, {ds_max})) ORDER BY calc_date'
        sql_statement = sql_base.format(site_id=site.id, ds_min=ds_min, ds_max=ds_max)
        query_base = ora.query(*col_names)
        result_set = query_base.from_statement(sql_statement).all()
        
        plot_parameters = ('date',)
        # get the pertinent columns from the dataframe
        if plot_sep:
            plot_parameters += (sandbar_disp_name,)
        else:
            if 'eddy' in calculation_types:
                plot_parameters += (eddy_total,)
            if 'chan' in calculation_types:
                plot_parameters += (channel_total,)
            if 'eddy_chan_sum' in calculation_types:
                plot_parameters += (total_site,)
        df_rs = create_pandas_dataframe(result_set, columns=(plot_parameters))
        df_pert_records = df_rs.to_dict('records')
        
        return self.render_to_csv_response(df_pert_records, plot_parameters)


class AreaVolumeCalcsDownloadView(CSVResponseMixin, View):
    
    """
    Output data that is more appropriate for a data dump
    rather than dygraphs.
    """
    
    model = AreaVolume
    
    def get(self, request, *args, **kwargs):
        
        site = Site.objects.get(pk=request.GET.get('site_id'))
        ds_min = float(request.GET.get('ds_min'))
        ds_max = float(request.GET.get('ds_max'))
        parent_params = request.GET.getlist('param_type')
        area_2d_calc_types = request.GET.getlist('area2d_calc_type')
        vol_calc_types = request.GET.getlist('volume_calc_type')
        sr_exists = site.deposit_type
        sr_ids = get_sep_reatt_ids(site.id)
        SandbarParams = namedtuple('SandbarParams', ['parameter', 'unit', 'sub_parameters'])
        param_list = []
        for parameter in parent_params:
            if parameter == 'area2d':
                unit = 'square meter'
                sub_p = area_2d_calc_types
            elif parameter == 'volume':
                unit = 'cubic meter'
                sub_p = vol_calc_types
            else:
                unit = None
                sub_p = None
            sbp = SandbarParams(parameter=parameter, unit=unit, sub_parameters=sub_p)
            param_list.append(sbp)
        acdb = AlchemDB()
        ora = acdb.create_session()
        sql_base = 'SELECT * FROM TABLE(SB_CALCS.F_GET_AREA_VOL_TF({site_id}, {ds_min}, {ds_max})) WHERE calc_type=:calc_type ORDER BY calc_date'
        sql_statement = sql_base.format(site_id=site.id, ds_min=ds_min, ds_max=ds_max)
        channel_total_str = '{p_name} Channel Total - {river_mile} {river_side} ({unit})'
        eddy_total_str = '{p_name} Eddy {sep_reatt} - {river_mile} {river_side} ({unit})'
        total_site_str = '{p_name} Total Site - {river_mile} {river_side} ({unit})'
        complete_dfs = []
        
        display_columns = [] # these are the columns that the user has specified for download
        for p_tuple in param_list:
            col_names = ('calc_date',) # keep track of the pertinent columns for a parameter (e.g. area or volume)
            sr_col_names = tuple() # keep track of intermediate columns needed to do math
            p_name = p_tuple.parameter
            sub_params = p_tuple.sub_parameters
            sandbar_id = 'sandbar_id'
            #query_base = ora.query('calc_date', sandbar_id, p_column)
            if p_name == 'area2d':
                area_display_name = 'Area'
                area_unit = 'square meter'
                a_channel_total = channel_total_str.format(p_name=area_display_name, river_mile=site.river_mile, river_side=site.river_side, unit=area_unit)
                if 'chan' in sub_params:
                    col_names += ('chan_int_area',) 
                    display_columns.append(a_channel_total)
                if 'eddy' in sub_params:
                    if sr_exists == 'SR':
                        col_names += ('eddy_s_int_area',)
                        col_names += ('eddy_r_int_area',)
                        col_names += ('sum_reatt_sep_area',)
                        a_eddy_s_total = eddy_total_str.format(p_name=area_display_name, sep_reatt='(Separation)', river_mile=site.river_mile, river_side=site.river_side, unit=area_unit)
                        a_eddy_r_total = eddy_total_str.format(p_name=area_display_name, sep_reatt='(Reattachment)', river_mile=site.river_mile, river_side=site.river_side, unit=area_unit)
                        a_eddy_sum_total = eddy_total_str.format(p_name=area_display_name, sep_reatt='Total', river_mile=site.river_mile, river_side=site.river_side, unit=area_unit)
                        display_columns.append(a_eddy_s_total)
                        display_columns.append(a_eddy_r_total)
                        display_columns.append(a_eddy_sum_total)
                    else:
                        col_names += ('eddy_int_area',)
                        a_eddy_total = eddy_total_str.format(p_name=area_display_name, sep_reatt='Total', river_mile=site.river_mile, river_side=site.river_side, unit=area_unit)
                        display_columns.append(a_eddy_total)
                a_total_site = total_site_str.format(p_name=area_display_name, river_mile=site.river_mile, river_side=site.river_side, unit=area_unit)
                if 'eddy_chan_sum' in sub_params:
                    display_columns.append(a_total_site)
                    col_names += ('ts_int_area',)
            if p_name == 'volume':
                vol_display_name = 'Volume'
                volume_unit = 'cubic meter'
                if 'chan' in sub_params:
                    col_names += ('chan_int_area',) 
                    display_columns.append(a_channel_total)
                v_channel_total_frag = channel_total_str.format(p_name=vol_display_name, river_mile=site.river_mile, river_side=site.river_side, unit=volume_unit)
                v_channel_total = display_name_base.format(param_frag=v_channel_total_frag, error_desc=error_bar_desc)
                sr_col_name = '{p_name} Eddy {sr_designation} ({unit}) {error_desc}'.format(
                                                                                                    p_name=vol_display_name, 
                                                                                                    sr_designation=create_sep_reatt_name(sr_id), 
                                                                                                    unit=volume_unit,
                                                                                                    error_desc=error_bar_desc
                                                                                                    )
                if 'chan' in sub_params:
                    display_columns.append(v_channel_total)
                v_eddy_total_frag = eddy_total_str.format(p_name=vol_display_name, river_mile=site.river_mile, river_side=site.river_side, unit=volume_unit)
                v_eddy_total = display_name_base.format(param_frag=v_eddy_total_frag, error_desc=error_bar_desc)
                if 'eddy' in sub_params:
                    display_columns.append(v_eddy_total)
                v_total_site_frag = total_site_str.format(p_name=vol_display_name, river_mile=site.river_mile, river_side=site.river_side, unit=volume_unit)
                v_total_site = display_name_base.format(param_frag=v_total_site_frag, error_desc=error_bar_desc)
                if 'eddy_chan_sum' in sub_params:
                    display_columns.append(v_total_site)
                query_base = ora.query('calc_date', 'sandbar_id', 'vol_error_low', 'interp_volume', 'vol_error_high')
                eddy_result_set = query_base.from_statement(sql_statement).params(calc_type='eddy').all()
                chan_result_set = query_base.from_statement(sql_statement).params(calc_type='chan').all()
                e_df0 = create_pandas_dataframe(eddy_result_set, columns=('date', 'sr_id', 'e_low', 'e_med', 'e_high'), create_psuedo_column=True)
                e_df0_float = e_df0.applymap(convert_to_float)
                c_df0 = create_pandas_dataframe(chan_result_set, columns=('date', 'sr_id', 'c_low', 'c_med', 'c_high'), create_psuedo_column=True)
                c_df0_float = c_df0.applymap(convert_to_float)
                c_df0_float[v_channel_total] = c_df0_float.apply(create_dygraphs_error_str, axis=1, low='c_low', med='c_med', high='c_high')
                c_df1 = c_df0_float[['date', 'c_low', 'c_med', 'c_high', v_channel_total]]
                sr_eddy_low = 'sr_eddy_low'
                sr_eddy_med = 'sr_eddy_med'
                sr_eddy_high = 'sr_eddy_high'
                eddy_col_names = (sr_eddy_low, sr_eddy_med, sr_eddy_high, v_eddy_total)
                if sr_exists:
                    sr_ids = get_sep_reatt_ids(site.id)
                    eddy_df_srs = []
                    for sr_id in sr_ids:
                        df_sr = e_df0_float[e_df0_float['sr_id'] == sr_id]
                        sr_col_name = '{p_name} Eddy {sr_designation} ({unit}) {error_desc}'.format(
                                                                                                    p_name=vol_display_name, 
                                                                                                    sr_designation=create_sep_reatt_name(sr_id), 
                                                                                                    unit=volume_unit,
                                                                                                    error_desc=error_bar_desc
                                                                                                    )
                        col_names += (sr_col_name,)
                        sr_col_names += (sr_col_name,)
                        df_sr[sr_col_name] = df_sr.applymap(round_series_values).apply(create_dygraphs_error_str, axis=1, low='e_low', med='e_med', high='e_high') # the dygraphs error string for one of the separation/reattachment sandbars
                        eddy_df_srs.append(df_sr)
                        if 'eddy' in sub_params:
                            display_columns.append(sr_col_name)
                    eddy_df_srs_len = len(eddy_df_srs)
                    col_names += (sr_eddy_low, sr_eddy_med, sr_eddy_high, v_eddy_total)
                    if eddy_df_srs_len == 1:
                        df_sr = eddy_df_srs[0]
                        df_sr[sr_eddy_low] = df_sr['e_low']
                        df_sr[sr_eddy_med] = df_sr['e_med']
                        df_sr[sr_eddy_high] = df_sr['e_high']
                        sep_reatt_col = sr_col_names[0]
                        df_sr[v_eddy_total] = df_sr[sep_reatt_col] # the dygraphs error string for combined separation/reattachment sandbars
                    elif eddy_df_srs_len == 2:
                        df_sr = pd.merge(eddy_df_srs[0], eddy_df_srs[1], how='outer', on='date').applymap(round_series_values) # combined separation/reattachment dataframe
                        df_sr[sr_eddy_low] = df_sr.apply(sum_two_columns, axis=1, col_x='e_low_x', col_y='e_low_y')
                        df_sr[sr_eddy_med] = df_sr.apply(sum_two_columns, axis=1, col_x='e_med_x', col_y='e_med_y')
                        df_sr[sr_eddy_high] = df_sr.apply(sum_two_columns, axis=1, col_x='e_high_x', col_y='e_high_y')
                        df_sr[v_eddy_total] = df_sr.apply(create_dygraphs_error_str, axis=1, low='sr_eddy_low', med='sr_eddy_med', high='sr_eddy_high') # the dygraphs error string for combined separation/reattachment sandbars
                    else:
                        raise Exception('Getting the separation/reattachment data went wrong...')
                    full_col_names = ('date',) + sr_col_names + eddy_col_names
                    e_df1 = df_sr[list(full_col_names)]
                else:
                    e_df0_float[sr_eddy_low] = e_df0_float['e_low']
                    e_df0_float[sr_eddy_med] = e_df0_float['e_med']
                    e_df0_float[sr_eddy_high] = e_df0_float['e_high']
                    e_df0_float[v_eddy_total] = e_df0_float.applymap(round_series_values).apply(create_dygraphs_error_str, axis=1, low=sr_eddy_low, med=sr_eddy_med, high=sr_eddy_high) # the dygraphs error string if separation/reattachment doesn't apply 
                    full_col_names = ('date', sr_eddy_low, sr_eddy_med, sr_eddy_high, v_eddy_total)
                    e_df1 = e_df0_float[list(full_col_names)]
                ec_merge = pd.merge(e_df1, c_df1, how='outer', on='date').applymap(round_series_values)
                ec_merge['ec_low'] = ec_merge.apply(sum_two_columns, axis=1, col_x=sr_eddy_low, col_y='c_low')
                ec_merge['ec_med'] = ec_merge.apply(sum_two_columns, axis=1, col_x=sr_eddy_med, col_y='c_med')
                ec_merge['ec_high'] = ec_merge.apply(sum_two_columns, axis=1, col_x=sr_eddy_high, col_y='c_high')
                ec_merge[v_total_site] = ec_merge.apply(create_dygraphs_error_str, axis=1, low='ec_low', med='ec_med', high='ec_high') # this is eddy + channel
                df_raw = ec_merge.where(pd.notnull(ec_merge), None)
                unneeded_columns = ('ec_low', 'ec_med', 'ec_high', sr_eddy_low, sr_eddy_med, sr_eddy_high, 'c_low', 'c_med', 'c_high')
                df_raw_columns = df_raw.columns.values
                needed_columns = tuple()
                for df_raw_col in df_raw_columns:
                    if df_raw_col not in unneeded_columns:
                        needed_columns += (df_raw_col,)
                df_volume = df_raw[list(needed_columns)]
                complete_dfs.append(df_volume)
            if p_name not in ('area2d', 'volume'):   
                raise Exception('I have no idea what you want me to query...')
        df_list_len = len(complete_dfs)
        if df_list_len == 1:
            df_merge = complete_dfs[0]
        elif df_list_len == 2:
            df_merge = pd.merge(complete_dfs[0], complete_dfs[1], how='outer', on='date')
        elif df_list_len >= 3:
            df_merge = pd.merge(complete_dfs[0], complete_dfs[1], how='outer', on='date')
            for df_object in complete_dfs[2:]:
                df_merge = pd.merge(df_merge, df_object, how='outer', on='date')
        else:
            df_merge = pd.DataFrame([])
        ora.close()
        try:
            df_raw = df_merge[pd.notnull(df_merge['date'])]
        except KeyError: # catch instances where df_merge is an empty dataframe
            df_raw = df_merge.copy()
        df_date = df_raw.applymap(datetime_to_date)
        df_ready = df_date.where(pd.notnull(df_date), None)
        display_column_list = ['date'] + sorted(display_columns)
        df_final = df_ready[display_column_list].sort(['date'])
        try:
            df_record = df_final.to_dict('records')
        except AttributeError:
            df_record = {}
        site_name = site.site_name.lower().replace(' ', '_')
        download_name = '{site_name}_min_{ds_min}_max_{ds_max}'.format(site_name=site_name, ds_min=ds_min, ds_max=ds_max)
        
        return self.render_to_csv_response(context=df_record, data_keys=display_column_list, download=True, download_name=download_name)      
        
                                      
class SitesListView(ListView):
    '''
    Extends ListView to serve site data including the min and max survey date. 
    '''
    
    template_name = 'surveys/site_list.html'
    model = Site
    
    context_object_name = 'site_list'
    
    
    def get_queryset(self):
        # The below should work but there is a bug in the Oracle database backend:
        # From the django test suite
        # get the following error because the SQL is ordered
        # by a geometry object, which Oracle apparently doesn't like:
        #  ORA-22901: cannot compare nested table or VARRAY or LOB attributes of an object type
        #        return self.model.objects.order_by('river_mile').annotate(min_survey_date=Min('survey__survey_date'), 
        #                                                                  max_survey_date=Max('survey__survey_date'))
        
        qs = self.model.objects.order_by('river_mile')
        
        result = []
        for site in qs:
            result.append({'site' : site,
                           'survey' : AreaVolume.objects.filter(site=site).aggregate(min_date=Min('calc_date'),
                                                                                 max_date=Max('calc_date'))})
        return result    


class SiteDetailView(DetailView):

    template_name = 'surveys/site.html'
    model = Site
    
    context_object_name = 'site'
    
    def get_context_data(self, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        return context


class GDAWSWebServiceProxy(SimpleWebServiceProxyView):
    ''' 
    Extends the SimpleWebServiceProxyView to implement the GDAWS service
    '''
    service_url = settings.GDAWS_SERVICE_URL
    

def _interpolateCalcs(xp, fp, Z):
    
    result = interp(Z, xp, fp);
    
    return result


class SandBarSitesGeoJSON(JSONResponseMixin, View):
    
    model = Site
    
    def get(self, request, *args, **kwargs):
        
        sites = Site.objects.all()
        feature_list = []
        for site_object in sites:
            try:
                latitude = site_object.geom.x
                longitude = site_object.geom.y
                point = create_geojson_point(latitude, longitude)
                feature_id = site_object.id
                feature = create_geojson_feature(point=point, feature_id=feature_id)
                feature_list.append(feature)
            except AttributeError: # handle instances where there is no geom data
                continue
        feature_collection = create_geojson_feature_collection(feature_list)
        
        return self.render_to_json_response(context=feature_collection)
    
    
class BasicSiteInfoJSON(JSONResponseMixin, View):
    
    model = AreaVolume
    
    def get(self, request, *args, **kwargs):
        
        site_id = request.GET.get('site_id')
        site_filter_set = AreaVolume.objects.filter(site_id=site_id)
        area_calc_date_min = site_filter_set.aggregate(Min('calc_date'))
        area_min_date_str = convert_datetime_to_str(area_calc_date_min['calc_date__min'])
        area_calc_date_max = site_filter_set.aggregate(Max('calc_date'))
        area_max_date_str = convert_datetime_to_str(area_calc_date_max['calc_date__max'])
        # check to see if site has separation and reattachment information
        distinct_sandbar_results = get_sep_reatt_ids(site_id)
        if len(distinct_sandbar_results) > 0:
            sr_list = distinct_sandbar_results
        else:
            sr_list = None
        site_info = {'siteID': site_id,
                     'calcDates': {'min': area_min_date_str,
                                  'max': area_max_date_str,},
                     'paramNames': {'area2d': 'Area of sandbar between lower and upper bound',
                                    'volume': 'Volume of sandbar between lower and upper bound'},
                     'sandbarIDs': sr_list
                     }
        return self.render_to_json_response(site_info)