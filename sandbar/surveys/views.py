from django.conf import settings
from django.db.models import Min, Max
from django.views.generic import ListView, DetailView, View, TemplateView
from numpy import interp
import pandas as pd 

from common.views import SimpleWebServiceProxyView
from common.utils.geojson_utils import create_geojson_point, create_geojson_feature, create_geojson_feature_collection
from .models import Site, Survey, AreaVolume
from .custom_mixins import CSVResponseMixin, JSONResponseMixin
from .db_utilities import convert_datetime_to_str, AlchemDB, replace_none_with_nan

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
        elif parameter_type == 'area3d':
            query_base = ora_session.query('calc_date', 'interp_area3d')
        elif parameter_type == 'volume':
            query_base = ora_session.query('calc_date', 'interp_volume')
        else:
            raise Exception('I have no idea what you want me to query...')
        for calculation_type in calculation_types:
            if calculation_type != 'eddy_chan_sum':
                query_result_set = query_base.from_statement(sql_statement).params(calc_type=calculation_type).all()
                df_value_name = '{calculation_type}_{param_type}'.format(calculation_type=calculation_type, param_type=parameter_type)
                query_df = pd.DataFrame(query_result_set, columns=('date', df_value_name))
            else:
                eddy_results = query_base.from_statement(sql_statement).params(calc_type='eddy').all()
                chan_results = query_base.from_statement(sql_statement).params(calc_type='chan').all()
                df_eddy = pd.DataFrame(eddy_results, columns=('date', 'eddy_value'))
                df_chan = pd.DataFrame(chan_results, columns=('date', 'chan_value'))
                df_ec_merge = pd.merge(df_eddy, df_chan, how='outer', on='date')
                df_values = df_ec_merge[['eddy_value', 'chan_value']]
                df_dates = df_ec_merge[['date']]
                df_values['eddy_channel_sum'] = df_values.sum(axis=1, skipna=True)
                query_df = pd.merge(df_dates, df_values, how='outer', left_index=True, right_index=True)
                query_df.drop(labels=['eddy_value', 'chan_value'], axis=1, inplace=True)
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
        column_name_tuple = (column_name_list.pop(0),)
        sorted_name_listed = sorted(column_name_list)
        sorted_name_tuple = tuple(sorted_name_listed)
        column_name_tuple += sorted_name_tuple
        
        df_record = df_merge.to_dict('records')
        
        return self.render_to_csv_response(context=df_record, data_keys=column_name_tuple)

                                      
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
        #site_id = context['site'].pk
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
                     'paramNames': {'area2d': 'Area 2D',
                                    'area3d': 'Area 3D'}
                     }
        return self.render_to_json_response(site_info)
    