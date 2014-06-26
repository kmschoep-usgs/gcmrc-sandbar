import pickle

from django.conf import settings
from django.db.models import Min, Max
from django.views.generic import ListView, DetailView, View
from numpy import interp 

from common.views import SimpleWebServiceProxyView
from common.utils.geojson_utils import create_geojson_point, create_geojson_feature, create_geojson_feature_collection
from .models import Site, Survey, AreaVolume
from .custom_mixins import CSVResponseMixin, JSONResponseMixin




class AreaVolumeCalcsView(CSVResponseMixin, View):
    
    model = AreaVolume
    
    def get(self, request, *args, **kwargs):
        #ds_min = 6500
        #ds_max = 9000
        # NOTE: will eventually pass in the ds_min/max as request.GET.get('ds_min')

        site = Site.objects.get(pk=request.GET.get('site_id'))
        ds_min = float(request.GET.get('ds_min'))
        ds_max = float(request.GET.get('ds_max'))
        elevationMin = str(site.elevationM(ds_min))
        elevationMax = str(site.elevationM(ds_max))
        qs = AreaVolume.objects.filter(site_id=site.id).filter(calc_type__iexact='eddy')
        pickle.dumps(qs)
        result = []
        for survey_date in qs.dates('calc_date', 'day'):
            d1 = qs.filter(calc_date=survey_date).filter(prev_plane_height__lte=elevationMin).filter(next_plane_height__gte=elevationMin).exclude(prev_plane_height__exact='0', plane_height__gte=elevationMin).order_by('plane_height')
            pickle.dumps(d1)
            if d1.exists():
                minAreaInt = _interpolateCalcs([float(d1[0].plane_height), float(d1[1].plane_height)] , [float(d1[0].area_2d_amt), float(d1[1].area_2d_amt)], float(elevationMin))
                d2 = qs.filter(calc_date=survey_date).filter(prev_plane_height__lte=elevationMax).filter(next_plane_height__gte=elevationMax).exclude(prev_plane_height__exact='0', plane_height__gte=elevationMax).order_by('plane_height')
                pickle.dumps(d2)
                if d2.exists():
                    maxAreaInt = _interpolateCalcs([float(d2[0].plane_height), float(d2[1].plane_height)] , [float(d2[0].area_2d_amt), float(d2[1].area_2d_amt)], float(elevationMax))
                    Area2d =  minAreaInt - maxAreaInt
                else:
                    Area2d = ''
            else:
                Area2d = ''
                
            survey_date_str = survey_date.strftime('%Y/%m/%d') 
            result.append({'Time' : survey_date_str, 'Area2d' : Area2d})
            
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
        site_id = context['site'].pk
        context['site_id'] = str(site_id)
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
    