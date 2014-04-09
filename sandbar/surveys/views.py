
from django.conf import settings
from django.db.models import Min, Max
from django.views.generic import ListView, DetailView, View
from django.db import connection
from django.http import Http404
#from factory.django import DjangoModelFactory

from common.views import SimpleWebServiceProxyView
from common.utils.view_utils import dictfetchall
from .models import Site, Survey, AreaVolume
from math import pow
from numpy import interp                                           

def _areaVolumeCalcs(site_id, coeffa, coeffb, coeffc, Q):
    
        Elev = _elevationM(coeffa, coeffb, coeffc, Q)
        
        area_volume = AreaVolume.objects.filter(site_id=site_id, prev_plane_height__lte=Elev, next_plane_height__gte=Elev).exclude(prev_plane_height__iexact=0)
        return area_volume.values('site_id',
                             'calc_date',
                             'calc_type',
                             'plane_height',
                             'area_2d_amt',
                             'area_3d_amt',
                             'volume_amt',
                             'prev_plane_height',
                             'next_plane_height')  
                                                    
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
    