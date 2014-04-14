
from django.conf import settings
from django.db.models import Min, Max, Q
from django.views.generic import ListView, DetailView, View
from django.db import connection
from django.http import Http404

from common.views import SimpleWebServiceProxyView
#from common.utils.view_utils import dictfetchall
from .models import Site, Survey, AreaVolume
from math import pow
from numpy import interp                                           

class AreaVolumeCalcsView(View):
    
    model = AreaVolume
    
    def get(self, request, *args, **kwargs):
        ds_min = 6500
        ds_max = 9000
        # NOTE: will eventually pass in the ds_min/max as request.GET.get('ds_min')

        site = Site.objects.get(pk=request.GET.get('site_id'))
        elevationMin = str(site.elevationM(ds_min))
        elevationMax = str(site.elevationM(ds_max))
        qs = AreaVolume.objects.filter(site_id=site.id).filter(calc_type__iexact='eddy')
        result = []
        for survey_date in qs.dates('calc_date', 'day'):
            d1 = qs.filter(calc_date=survey_date).filter(prev_plane_height__lte=elevationMin).filter(next_plane_height__gte=elevationMin).exclude(prev_plane_height__exact='0', plane_height__gte=elevationMin).order_by('plane_height')
            if d1.exists():
                minAreaInt = _interpolateCalcs([d1[0].plane_height, d1[1].plane_height] , [d1[0].area_2d_amt, d1[1].area_2d_amt], elevationMin)
                '''
                d2 = qs.filter(calc_date=survey_date).filter(prev_plane_height__lte=elevationMax).filter(next_plane_height__gte=elevationMax).exclude(prev_plane_height__exact='0', plane_height__gte=elevationMax).order_by('plane_height')
                if d2.exists():
                    maxAreaInt = _interpolateCalcs([d2.plane_height[0], d2.plane_height[1]] , [d2.area_2d_amt[0], d2.area_2d_amt[1]], elevationMax)
                    Area2d = maxAreaInt - minAreaInt
                    result.append({'Time' : survey_date,
                                   'Area2d' : Area2d})
                '''
        return minAreaInt    

                                      
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



class GDAWSWebServiceProxy(SimpleWebServiceProxyView):
    ''' 
    Extends the SimpleWebServiceProxyView to implement the GDAWS service
    '''
    service_url = settings.GDAWS_SERVICE_URL
    

def _interpolateCalcs(xp, fp, Z):
    
    result = interp(Z, xp, fp);
    
    return result
    