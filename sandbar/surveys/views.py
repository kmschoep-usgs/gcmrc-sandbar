from collections import namedtuple

from django.conf import settings
from django.db.models import Min, Max
from django.views.generic import ListView, DetailView, View, TemplateView
from numpy import interp
import pandas as pd 

from common.views import SimpleWebServiceProxyView
from common.utils.geojson_utils import create_geojson_point, create_geojson_feature, create_geojson_feature_collection
from .models import Site, Survey, AreaVolume
from .custom_mixins import CSVResponseMixin, JSONResponseMixin
from .db_utilities import convert_datetime_to_str, AlchemDB
from .pandas_utils import (create_pandas_dataframe, round_series_values, datetime_to_date, create_df_error_bars, 
                           col_difference, sum_two_columns, create_dygraphs_error_str)

class AreaVolumeCalcsTemp(TemplateView):
    
    template_name = 'surveys/expt.html'
    
    def get(self, request, *args, **kwargs):
        #ds_min = 6500
        #ds_max = 9000
        # NOTE: will eventually pass in the ds_min/max as request.GET.get('ds_min')

        result = []

        site = Site.objects.get(pk=request.GET.get('site_id'))
        ds_min = float(request.GET.get('ds_min'))
        ds_max = float(request.GET.get('ds_max'))
        calculation_type = request.GET.get('calc_type', None)
        alchemical_sql = AlchemDB()
        sql_base = 'SELECT * FROM TABLE(get_area_vol_tf({site_id}, {ds_min}, {ds_max})) WHERE calc_type=:calc_type ORDER BY calc_date'
        sql_statement = sql_base.format(site_id=site.id, ds_min=ds_min, ds_max=ds_max)
        ora_session = alchemical_sql.create_session()
        query_results = ora_session.query('calc_date', 'interp_area2d').from_statement(sql_statement).params(calc_type=calculation_type)
        for query_result in query_results:
            date, interp_area_2d = query_result
            date_str = date.strftime('%Y/%m/%d')
            result_dict = {'Time': date_str, 'Area2d': interp_area_2d}
            result.append(result_dict)
            
        context = {'result_dict': result}
        
        return self.render_to_response(context)


class AreaVolumeCalcsView(CSVResponseMixin, View):
    
    """
    Output data that is appropriate for dygraphs
    ingestion.
    """
    
    model = AreaVolume
    
    def get(self, request, *args, **kwargs):
        #ds_min = 6500
        #ds_max = 9000
        # NOTE: will eventually pass in the ds_min/max as request.GET.get('ds_min')
        
        site = Site.objects.get(pk=request.GET.get('site_id'))
        ds_min = float(request.GET.get('ds_min'))
        ds_max = float(request.GET.get('ds_max'))
        parameter_type = request.GET.get('param_type')
        calculation_types = request.GET.getlist('calc_type', None)
        alchemical_sql = AlchemDB()
        sql_base = 'SELECT * FROM TABLE(get_area_vol_tf({site_id}, {ds_min}, {ds_max})) WHERE calc_type=:calc_type ORDER BY calc_date'
        sql_statement = sql_base.format(site_id=site.id, ds_min=ds_min, ds_max=ds_max)
        ora_session = alchemical_sql.create_session()
        df_list = []
        if parameter_type == 'area2d':
            query_base = ora_session.query('calc_date', 'interp_area2d')
        elif parameter_type == 'volume':
            query_base = ora_session.query('calc_date', 'vol_error_low', 'interp_volume', 'vol_error_high')
        else:
            raise Exception('I have no idea what you want me to query...')
        for calculation_type in calculation_types:
            if calculation_type != 'eddy_chan_sum':
                query_result_set = query_base.from_statement(sql_statement).params(calc_type=calculation_type).all()
                if calculation_type == 'chan':
                    calculation_type_full = 'channel'
                    df_value_name = calculation_type_full.title()
                else:
                    df_value_name = calculation_type.title()
                if parameter_type == 'volume':
                    query_df = create_df_error_bars(data=query_result_set, final_col_name=df_value_name)
                else:
                    query_df = create_pandas_dataframe(data=query_result_set, columns=('date', df_value_name))
            elif calculation_type == 'eddy_chan_sum' and parameter_type == 'area2d':
                eddy_results = query_base.from_statement(sql_statement).params(calc_type='eddy').all()
                chan_results = query_base.from_statement(sql_statement).params(calc_type='chan').all()
                df_eddy = create_pandas_dataframe(data=eddy_results, columns=('date', 'Eddy'), create_psuedo_column=True)
                df_chan = create_pandas_dataframe(data=chan_results, columns=('date', 'Channel'), create_psuedo_column=True)
                df_ec_merge = pd.merge(df_eddy, df_chan, how='outer', on='date')
                # separate the eddy and channel values from the date for summation
                df_values = df_ec_merge[['Eddy', 'Channel']]
                # create a date dataframe
                df_dates = df_ec_merge[['date']]
                df_values['Total Site'] = df_values.sum(axis=1, skipna=True)
                # merge our dataframe back together based on row index
                query_df = pd.merge(df_dates, df_values, how='outer', left_index=True, right_index=True)
                query_df.drop(labels=['Eddy', 'Channel'], axis=1, inplace=True)
                # remove any dates that are NaT (not a datetime) or NaN (not a number) in the date column
                query_df = query_df[pd.notnull(query_df['date'])]
            elif calculation_type == 'eddy_chan_sum' and parameter_type == 'volume':
                eddy_results = query_base.from_statement(sql_statement).params(calc_type='eddy').all()
                chan_results = query_base.from_statement(sql_statement).params(calc_type='chan').all()
                df_eddy = create_pandas_dataframe(data=eddy_results, columns=('date', 'e_vol_low', 'e_vol_val', 'e_vol_high'), create_psuedo_column=True)
                df_chan = create_pandas_dataframe(data=chan_results, columns=('date', 'c_vol_low', 'c_vol_val', 'c_vol_high'), create_psuedo_column=True)
                df_ec_merge = pd.merge(df_eddy, df_chan, how='outer', on='date')
                df_ec_merge['e_low_delta'] = df_ec_merge.apply(col_difference, axis=1, args=('e_vol_val', 'e_vol_low'))
                df_ec_merge['e_high_delta'] = df_ec_merge.apply(col_difference, axis=1, args=('e_vol_high', 'e_vol_val'))
                df_ec_merge['c_low_delta'] = df_ec_merge.apply(col_difference, axis=1, args=('c_vol_val', 'c_vol_low'))
                df_ec_merge['c_high_delta'] = df_ec_merge.apply(col_difference, axis=1, args=('c_vol_high', 'c_vol_val'))
                df_ec_merge['ec_low_delta'] = df_ec_merge.apply(sum_two_columns, axis=1, args=('e_low_delta', 'c_low_delta'))
                df_ec_merge['ec_high_delta'] = df_ec_merge.apply(sum_two_columns, axis=1, args=('e_high_delta', 'c_high_delta'))
                df_ec_merge['ec_sum'] = df_ec_merge.apply(sum_two_columns, axis=1, args=('e_vol_val', 'c_vol_val'))
                df_ec_merge['ec_lower'] = df_ec_merge.apply(col_difference, axis=1, args=('ec_sum', 'ec_low_delta'))
                df_ec_merge['ec_high'] = df_ec_merge.apply(sum_two_columns, axis=1, args=('ec_sum', 'ec_high_delta'))
                df_ec_merge['Total Site'] = df_ec_merge.apply(create_dygraphs_error_str, axis=1, low='ec_lower', med='ec_sum', high='ec_high')
                df_ec_merge_clean = df_ec_merge[pd.notnull(df_ec_merge['date'])]
                query_df = df_ec_merge_clean[['date', 'Total Site']]
            else:
                raise Exception('Something went terribly wrong...')          
            if len(query_df) > 0:
                df_list.append(query_df)
        df_list_len = len(df_list)
        if df_list_len == 1:
            df_merge = df_list[0]
        elif df_list_len == 2:
            df_merge = pd.merge(df_list[0], df_list[1], how='outer', on='date')
        elif df_list_len >= 3:
            df_merge = pd.merge(df_list[0], df_list[1], how='outer', on='date')
            for df_object in df_list[2:]:
                df_merge = pd.merge(df_merge, df_object, how='outer', on='date')
        else:
            df_merge = pd.DataFrame([])
        ora_session.close()
        column_name_array = df_merge.columns.values
        column_name_list = list(column_name_array)
        try:
            column_name_tuple = (column_name_list.pop(0),)
        except(IndexError):
            column_name_tuple = (None,)
        sorted_name_listed = sorted(column_name_list)
        sorted_name_tuple = tuple(sorted_name_listed)
        column_name_tuple += sorted_name_tuple
        df_final = df_merge.where(pd.notnull(df_merge), None)
        
        df_record = df_final.to_dict('records')
        
        return self.render_to_csv_response(context=df_record, data_keys=column_name_tuple)
    

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
        SandbarParams = namedtuple('SandbarParams', ['parameter', 'db_column', 'unit', 'sub_parameters'])
        param_list = []
        for parameter in parent_params:
            if parameter == 'area2d':
                db_column = 'interp_area2d'
                unit = 'square meter'
                sub_p = area_2d_calc_types
            elif parameter == 'volume':
                db_column = 'interp_volume'
                unit = 'cubic meter'
                sub_p = vol_calc_types
            else:
                db_column = None
                unit = None
                sub_p = None
            sbp = SandbarParams(parameter=parameter, db_column=db_column, unit=unit, sub_parameters=sub_p)
            param_list.append(sbp)
        alchemical_sql = AlchemDB()
        ora_session = alchemical_sql.create_session()
        sql_base = 'SELECT * FROM TABLE(get_area_vol_tf({site_id}, {ds_min}, {ds_max})) WHERE calc_type=:calc_type ORDER BY calc_date'
        sql_statement = sql_base.format(site_id=site.id, ds_min=ds_min, ds_max=ds_max)
        complete_dfs = []
        for p_tuple in param_list:
            p_name = p_tuple.parameter
            p_column = p_tuple.db_column
            p_subp = p_tuple.sub_parameters
            p_unit = p_tuple.unit
            query_base = ora_session.query('calc_date', p_column)
            for subp in p_subp:
                if subp != 'eddy_chan_sum':
                    calc_qs = query_base.from_statement(sql_statement).params(calc_type=subp).all()
                    column_name = '{parent_name}_{calc_type} ({unit})'.format(parent_name=p_name, calc_type=subp, unit=p_unit)
                    calc_df = create_pandas_dataframe(calc_qs, ('date', column_name), True)
                else:
                    eddy_results = query_base.from_statement(sql_statement).params(calc_type='eddy').all()
                    chan_results = query_base.from_statement(sql_statement).params(calc_type='chan').all()
                    eddy_name = '%s_eddy' % p_name
                    chan_name = '%s_chan' % p_name
                    df_eddy = create_pandas_dataframe(data=eddy_results, columns=('date', eddy_name), create_psuedo_column=True)
                    df_chan = create_pandas_dataframe(data=chan_results, columns=('date', chan_name), create_psuedo_column=True)
                    df_ec_merge = pd.merge(df_eddy, df_chan, how='outer', on='date')
                    df_values = df_ec_merge[[eddy_name, chan_name]]
                    df_dates = df_ec_merge[['date']]
                    df_total_sites_name = '{parent_name}_total_site ({unit})'.format(parent_name=p_name, unit=p_unit)
                    df_values[df_total_sites_name] = df_values.sum(axis=1, skipna=True)                   
                    query_df = pd.merge(df_dates, df_values, how='outer', left_index=True, right_index=True)
                    query_df.drop(labels=[eddy_name, chan_name], axis=1, inplace=True)
                    calc_df = query_df[pd.notnull(query_df['date'])]
                if len(calc_df) > 0:
                    complete_dfs.append(calc_df)
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
        ora_session.close()
        column_name_array = df_merge.columns.values
        column_name_list = list(column_name_array)
        try:
            column_name_tuple = (column_name_list.pop(0),)
        except(IndexError):
            column_name_tuple = (None,)
        sorted_name_listed = sorted(column_name_list)
        sorted_name_tuple = tuple(sorted_name_listed)
        column_name_tuple += sorted_name_tuple
        df_final_raw = df_merge[pd.notnull(df_merge['date'])]
        df_final_rounded = df_final_raw.applymap(round_series_values).applymap(datetime_to_date)
        df_final = df_final_rounded.where(pd.notnull(df_final_rounded), None)
        df_record = df_final.to_dict('records')
        site_name = site.site_name.lower().replace(' ', '_')
        download_name = '{site_name}_min_{ds_min}_max_{ds_max}'.format(site_name=site_name, ds_min=ds_min, ds_max=ds_max)
        
        return self.render_to_csv_response(context=df_record, data_keys=column_name_tuple, download=True, download_name=download_name)      
        
                                      
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
                           'survey' : Survey.objects.filter(site=site).aggregate(min_date=Min('survey_date'),
                                                                                 max_date=Max('survey_date'))})
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
            latitude = site_object.geom.x
            longitude = site_object.geom.y
            point = create_geojson_point(latitude, longitude)
            feature_id = site_object.id
            feature = create_geojson_feature(point=point, feature_id=feature_id)
            feature_list.append(feature)
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
        site_info = {'siteID': site_id,
                     'calcDates': {'min': area_min_date_str,
                                  'max': area_max_date_str,},
                     'paramNames': {'area2d': 'Area of sandbar between lower and upper bound',
                                    'volume': 'Volume of sandbar between lower and upper bound'}
                     }
        return self.render_to_json_response(site_info)
    
