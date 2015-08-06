from collections import namedtuple
from string import Template

from django.conf import settings
from django.db.models import Min, Max
from django.views.generic import ListView, DetailView, View
from numpy import interp

from common.views import SimpleWebServiceProxyView
from common.utils.geojson_utils import create_geojson_point, create_geojson_feature, create_geojson_feature_collection
from .models import Site, AreaVolume, AreaVolumeOutput, Sandbar
from .custom_mixins import CSVResponseMixin, JSONResponseMixin
from .db_utilities import convert_datetime_to_str, AlchemDB, get_sep_reatt_ids
from .pandas_utils import create_pandas_dataframe, round_series_values, datetime_to_date, convert_to_str, create_sep_reatt_name


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
        result_len = len(result_set)
        
        plot_parameters = ()
        if result_len != 0:
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
        river_mile = site.river_mile
        river_side = site.river_side
        ds_min = float(request.GET.get('ds_min'))
        ds_max = float(request.GET.get('ds_max'))
        parent_params = request.GET.getlist('param_type')
        area_2d_calc_types = request.GET.getlist('area2d_calc_type')
        vol_calc_types = request.GET.getlist('volume_calc_type')
        sr_exists = site.deposit_type
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
        sql_base = 'SELECT * FROM TABLE(SB_CALCS.F_GET_AREA_VOL_TF({site_id}, {ds_min}, {ds_max})) ORDER BY calc_date'
        sql_statement = sql_base.format(site_id=site.id, ds_min=ds_min, ds_max=ds_max)
        col_names = ('calc_date',) # keep track of the pertinent columns for a parameter (e.g. area or volume)
        display_columns = ['Date',]
        reatt = 'Reattachment'
        seprt = 'Separation'
        total = 'Total'
        
        for p_tuple in param_list:
            p_name = p_tuple.parameter
            sub_params = p_tuple.sub_parameters
            if p_name == 'area2d':
                area_display_name = 'Area'
                area_unit = p_tuple.unit
                area_sub = {'p_name': area_display_name,
                            'river_mile': river_mile,
                            'river_side': river_side,
                            'unit': area_unit,
                            }
                channel_total_str = Template('$p_name Channel Total - $river_mile $river_side ($unit)').safe_substitute(area_sub)
                eddy_total_str = Template('$p_name Eddy ({sr_type}) - $river_mile $river_side ($unit)').safe_substitute(area_sub)
                total_site_str = Template('$p_name Total Site - $river_mile $river_side ($unit)').safe_substitute(area_sub)
                a_channel_total = channel_total_str
                if 'chan' in sub_params:
                    col_names += ('chan_int_area',) 
                    display_columns.append(a_channel_total)
                if 'eddy' in sub_params:
                    if sr_exists == 'SR':
                        col_names += ('eddy_s_int_area', 'eddy_r_int_area', 'sum_reatt_sep_area')
                        a_eddy_s_total = eddy_total_str.format(sr_type=seprt)
                        a_eddy_r_total = eddy_total_str.format(sr_type=reatt)
                        a_eddy_sum_total = eddy_total_str.format(sr_type=total)
                        display_columns.append(a_eddy_s_total)
                        display_columns.append(a_eddy_r_total)
                        display_columns.append(a_eddy_sum_total)
                    else:
                        col_names += ('eddy_int_area',)
                        a_eddy_total = eddy_total_str.format(sr_type=total)
                        display_columns.append(a_eddy_total)
                if 'eddy_chan_sum' in sub_params:
                    col_names += ('ts_int_area',)
                    a_total_site = total_site_str
                    display_columns.append(a_total_site)
            if p_name == 'volume':
                lower = 'Lower'
                upper = 'Upper'
                vol_unit = p_tuple.unit
                vol_sub = {'river_mile': river_mile,
                           'river_side': river_side,
                           'unit': vol_unit
                           }
                error_template = Template('{calc} Volume Error {bound} Bound - $river_mile $river_side ($unit)').safe_substitute(vol_sub)
                measured_str = Template('{calc} Volume Measured Value - $river_mile $river_side ($unit)').safe_substitute(vol_sub)
                if 'chan' in sub_params:
                    calc_name = 'Channel'
                    col_names += ('chan_vol_error_low', 'chan_int_volume', 'chan_vol_error_high')
                    chan_vel_name = error_template.format(calc=calc_name, bound=lower)
                    chan_vol_name = measured_str.format(calc=calc_name)
                    chan_veh_name = error_template.format(calc=calc_name, bound=upper)
                    display_columns.append(chan_vel_name)
                    display_columns.append(chan_vol_name)
                    display_columns.append(chan_veh_name)
                if 'eddy' in sub_params:
                    calc_name = 'Eddy'
                    if sr_exists == 'SR':
                        sr_error_str = Template('Eddy Volume ({sr_type}) {bound} Bound - $river_mile $river_side ($unit)').safe_substitute(vol_sub)
                        sr_measured_str = Template('Eddy Volume ({sr_type}) Measured Value - $river_mile $river_side ($unit)').safe_substitute(vol_sub)
                        eddy_reattachment_cols = ('eddy_r_vol_error_low', 'eddy_r_int_volume', 'eddy_r_vol_error_high')
                        eddy_reattachement_names = [sr_error_str.format(sr_type=reatt, bound=lower),
                                                    sr_measured_str.format(sr_type=reatt),
                                                    sr_error_str.format(sr_type=reatt, bound=upper)
                                                    ]
                        display_columns += eddy_reattachement_names
                        eddy_separation_cols = ('eddy_s_vol_error_low', 'eddy_s_int_volume', 'eddy_s_vol_error_high')
                        eddy_separation_names = [sr_error_str.format(sr_type=seprt, bound=lower),
                                                 sr_measured_str.format(sr_type=seprt),
                                                 sr_error_str.format(sr_type=seprt, bound=upper)
                                                 ]
                        display_columns += eddy_separation_names
                        eddy_sr_sum_cols = ('sum_reatt_sep_vel', 'sum_reatt_sep_vol', 'sum_reatt_sep_veh')
                        sr_sum_names = [sr_error_str.format(sr_type=total, bound=lower),
                                        sr_measured_str.format(sr_type=total),
                                        sr_error_str.format(sr_type=total, bound=upper)
                                        ]
                        display_columns += sr_sum_names
                        col_names += eddy_reattachment_cols + eddy_separation_cols + eddy_sr_sum_cols
                    else:
                        col_names += ('eddy_vol_error_low', 'eddy_int_volume', 'eddy_vol_error_high')
                        eddy_vel_name = error_template.format(calc=calc_name, bound=lower)
                        eddy_vol_name = measured_str.format(calc=calc_name)
                        eddy_veh_name = error_template.format(calc=calc_name, bound=upper)
                        display_columns.append(eddy_vel_name)
                        display_columns.append(eddy_vol_name)
                        display_columns.append(eddy_veh_name)
                if 'eddy_chan_sum' in sub_params:
                    volume_total_site_error_str = Template('Volume Total Site {bound} - $river_mile $river_side ($unit)').safe_substitute(vol_sub)
                    col_names += ('ts_vol_error_low', 'ts_int_volume', 'ts_vol_error_high')
                    volume_total_names = [volume_total_site_error_str.format(bound='Lower Bound'),
                                          volume_total_site_error_str.format(bound='Measured Value'),
                                          volume_total_site_error_str.format(bound='Upper Bound')
                                          ]
                    display_columns += volume_total_names
            query_base = ora.query(*col_names)
            result_set = query_base.from_statement(sql_statement).all()
            df_rs = create_pandas_dataframe(result_set, columns=display_columns)
            df_rs_clean = df_rs.applymap(round_series_values).applymap(datetime_to_date).applymap(convert_to_str)
            df_record = df_rs_clean.to_dict('records')
            site_name = site.site_name.lower().replace(' ', '_')
            download_name = '{site_name}_min_{ds_min}_max_{ds_max}'.format(site_name=site_name,
                                                                           ds_min=ds_min,
                                                                           ds_max=ds_max)
        return self.render_to_csv_response(context=df_record, data_keys=display_columns, 
                                           download=True, download_name=download_name)      
        
                                      
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