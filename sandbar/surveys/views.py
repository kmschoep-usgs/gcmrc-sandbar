from collections import namedtuple

from django.conf import settings
from django.db.models import Min, Max
from django.views.generic import ListView, DetailView, View, TemplateView
from numpy import interp 

from common.views import SimpleWebServiceProxyView
from common.utils.geojson_utils import create_geojson_point, create_geojson_feature, create_geojson_feature_collection
from .models import Site, Survey, AreaVolume
from .custom_mixins import CSVResponseMixin, JSONResponseMixin
from .db_utilities import convert_datetime_to_str, AlchemDB

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
        
        result = []

        site = Site.objects.get(pk=request.GET.get('site_id'))
        ds_min = float(request.GET.get('ds_min'))
        ds_max = float(request.GET.get('ds_max'))
        calculation_type = request.GET.get('calc_type', None)
        alchemical_sql = AlchemDB()
        sql_base = 'SELECT * FROM TABLE(get_area_vol_tf({site_id}, {ds_min}, {ds_max})) WHERE calc_type=:calc_type ORDER BY calc_date'
        sql_statement = sql_base.format(site_id=site.id, ds_min=ds_min, ds_max=ds_max)
        ora_session = alchemical_sql.create_session()
        if calculation_type == 'eddy':
            query_results = ora_session.query('calc_date', 'interp_area2d').from_statement(sql_statement).params(calc_type='eddy')
        elif calculation_type == 'chan':
            query_results = ora_session.query('calc_date', 'interp_area2d').from_statement(sql_statement).params(calc_type='chan')
        elif calculation_type == 'eddy_chan_sum':
            eddy_results = ora_session.query('calc_date', 'interp_area2d').from_statement(sql_statement).params(calc_type='eddy').all()
            chan_results = ora_session.query('calc_date', 'interp_area2d').from_statement(sql_statement).params(calc_type='chan').all()
            full_dates = []
            for e_record in eddy_results:
                e_date = e_record[0]
                full_dates.append(e_date)
            for c_record in chan_results:
                c_date = c_record[0]
                full_dates.append(c_date)
            date_set = set(full_dates)
            distinct_dates = list(date_set)
            sorted_distinct_dates = sorted(distinct_dates)
            combined_results = []
            query_results = []
            for distinct_date in sorted_distinct_dates:
                CombinedResults = namedtuple('CombinedResults', ['calc_date', 'eddy_value', 'chan_value'])
                cr_tuple = CombinedResults(calc_date=distinct_date, eddy_value=None, chan_value=None)
                for eddy_result in eddy_results:
                    eddy_date, eddy_val = eddy_result
                    if eddy_date == distinct_date:
                        cr_tuple = cr_tuple._replace(eddy_value=eddy_val)
                for chan_result in chan_results:
                    chan_date, chan_val = chan_result
                    if chan_date == distinct_date:
                        cr_tuple = cr_tuple._replace(chan_value=chan_val)
                combined_results.append(cr_tuple)
            #sum eddy and channel values
            for combined_result in combined_results:
                measurement_date = combined_result.calc_date
                cr_eddy_val = combined_result.eddy_value
                cr_chan_val = combined_result.chan_value
                # handle NaNs in the summation of eddy and channel
                if cr_eddy_val and cr_chan_val:
                    cev = cr_eddy_val
                    ccv = cr_chan_val
                elif cr_eddy_val is None and cr_chan_val is not None:
                    cev = 0
                    ccv = cr_chan_val
                elif cr_eddy_val is not None and cr_chan_val is None:
                    cev = cr_eddy_val
                    ccv = 0
                elif cr_eddy_val is None and cr_chan_val is None:
                    cev = None
                    ccv = None
                else:
                    cev = 0
                    ccv = 0
                try:
                    cr_sum = cev + ccv
                    cr_tuple = (measurement_date, cr_sum)
                    query_results.append(cr_tuple)
                except TypeError:
                    cr_tuple = (measurement_date, None)
                    query_results.append(cr_tuple)    
        else:
            query_results = []
        
        for query_result in query_results:
            date, interp_area_2d = query_result
            date_str = date.strftime('%Y/%m/%d')
            result_dict = {'Time': date_str, 'Area2d': interp_area_2d}
            result.append(result_dict)
        ora_session.close()  
        data_keys = ['Time', 'Area2d']
        
        return self.render_to_csv_response(context=result, data_keys=data_keys)

                                      
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
        #context['site'] = str(site_id)
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
    