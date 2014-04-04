
from django.conf import settings
from django.db.models import Min, Max, F, Q
from django.views.generic import ListView, DetailView, View
from django.db import connection
from urllib2 import urlopen, HTTPError
from django.http import HttpResponse

from common.views import SimpleWebServiceProxyView
from common.utils.view_utils import dictfetchall
from .models import Site, Survey
from math import pow
from numpy import interp

def _area_volume_qs(site_id, min_elev, max_elev):
    
    query = 'select \
AV.SITE_ID, \
AV.SANDBAR_ID, \
av.calc_date, \
av.calc_type, \
av2.calc_type, \
AV.PLANE_HEIGHT survey, \
AV2.PLANE_HEIGHT min_surf, \
AV.AREA_2D_AMT  - AV2.AREA_2D_AMT area2d, \
AV.AREA_2D_AMT - AV2.AREA_3D_AMT area3d, \
AV.VOLUME_AMT - AV2.VOLUME_AMT vol \
from AREA_VOLUME_CALC av, AREA_VOLUME_CALC av2 \
where AV.CALC_DATE = AV.CALC_DATE \
 and ((AV.CALC_TYPE = \'chan\' and \
 AV2.CALC_TYPE = \'minchan\') or \
  (AV.CALC_TYPE = \'eddy\' and \
 AV2.CALC_TYPE = \'mineddy\')) and \
 av.site_id = av2.site_id and \
 av.site_id = %s and \
 nvl(av.sandbar_id,-9) = nvl(av2.sandbar_id,-9) \
 and av.plane_height between %s and %s \
 and av2.plane_height = \
    (select min(av3.plane_height) from area_volume_calc av3 \
        where av3.calc_date = av.calc_date and \
        av3.calc_type in (\'eddy\',\'chan\') and \
        av.site_id = av3.site_id and \
        nvl(av.sandbar_id,-9) = nvl(av3.sandbar_id,-9) \
        ) \
order by av.calc_date, av.plane_height;' %(site_id, min_elev, max_elev)
        
    cursor = connection.cursor() #@UndefinedVariable
    cursor.execute(query)
    results_list = dictfetchall(cursor)
    return results_list
                                            
                                            
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
    
    
    def get(self, request, *args, **kwargs):
        ''' Override get_object to return the site details and area/volume calculation.
        The returned object is a dictionary.
        '''
        site_id = self.kwargs.get('pk')
        site_qs = Site.objects.get(pk=site_id)
        coeffa = float(site_qs.stage_discharge_coeff_a)
        coeffb = float(site_qs.stage_discharge_coeff_b)
        coeffc = float(site_qs.stage_discharge_coeff_c)
        minElev = _elevationM(coeffa, coeffb, coeffc, 150)
        maxElev = _elevationM(coeffa, coeffb, coeffc, 1150)
        

        query = 'select \
AV.SITE_ID, \
AV.SANDBAR_ID, \
av.calc_date, \
av.calc_type, \
av2.calc_type, \
AV.PLANE_HEIGHT survey, \
AV2.PLANE_HEIGHT min_surf, \
AV.AREA_2D_AMT  - AV2.AREA_2D_AMT area2d, \
AV.AREA_2D_AMT - AV2.AREA_3D_AMT area3d, \
AV.VOLUME_AMT - AV2.VOLUME_AMT vol \
from AREA_VOLUME_CALC av, AREA_VOLUME_CALC av2 \
where AV.CALC_DATE = AV.CALC_DATE \
 and ((AV.CALC_TYPE = \'chan\' and \
 AV2.CALC_TYPE = \'minchan\') or \
  (AV.CALC_TYPE = \'eddy\' and \
 AV2.CALC_TYPE = \'mineddy\')) and \
 av.site_id = av2.site_id and \
 av.site_id = %s and \
 nvl(av.sandbar_id,-9) = nvl(av2.sandbar_id,-9) \
 and av.plane_height between %s and %s \
 and av2.plane_height = \
    (select min(av3.plane_height) from area_volume_calc av3 \
        where av3.calc_date = av.calc_date and \
        av3.calc_type in (\'eddy\',\'chan\') and \
        av.site_id = av3.site_id and \
        nvl(av.sandbar_id,-9) = nvl(av3.sandbar_id,-9) \
        ) \
order by av.calc_date, av.plane_height;' %(site_id, minElev, maxElev)
        
        cursor = connection.cursor() #@UndefinedVariable
        cursor.execute(query)
        results_list = dictfetchall(cursor)
        results = {};
        results['areaVolume'] = []
        for av in results_list:
            results['areaVolume'].append({'area_vol' : av})
        return HttpResponse(results['areaVolume'])
               
class GDAWSWebServiceProxy(SimpleWebServiceProxyView):
    ''' 
    Extends the SimpleWebServiceProxyView to implement the GDAWS service
    '''
    service_url = settings.GDAWS_SERVICE_URL
    
def _elevationM(a,b,c,Q):
    '''
    Equation:
    Z=a+b*Q-c*Q^2
    where,
    Z = elevation, in meters
    Q is discharge in cfs

    inputs:
    Q = user input
    a = sites.STAGE_DISCHARGE_COEFF_A
    b = sites.STAGE_DISCHARGE_COEFF_B
    c = sites.STAGE_DISCHARGE_COEFF_C

    The resulting Z-range is compared to area_volume_calc.plane_height.
    '''
    result = a+b*Q-c*pow(Q,2);

    return result

def _interpolateCalcs(xp, fp, Z):
    
    result = interp(Z, xp, fp);
    
    return result
    