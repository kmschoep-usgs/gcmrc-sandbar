import pickle

from django.conf import settings
from django.db.models import Min, Max
from django.views.generic import ListView, DetailView, View, TemplateView
from numpy import interp 
from sqlalchemy import func

from common.views import SimpleWebServiceProxyView
from .models import Site, Survey, AreaVolume
from .custom_mixins import CSVResponseMixin
from .db_mappings import AreaVolumeCalcBase
from .db_utilities import QueryDB

try:
    from sandbar_project.local_settings import SCHEMA_USER, DB_PWD, DB_DESC
except ImportError:
    SCHEMA_USER = None
    DB_PWD = None
    DB_DESC = None



class AreaVolumeCalcsView(CSVResponseMixin, View):
    
    model = AreaVolume
    
    def get(self, request, *args, **kwargs):
        ds_min = 6500
        ds_max = 9000
        # NOTE: will eventually pass in the ds_min/max as request.GET.get('ds_min')

        site = Site.objects.get(pk=request.GET.get('site_id'))
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
                    Area2d = maxAreaInt - minAreaInt
                else:
                    Area2d = ''
            else:
                Area2d = ''
                
            survey_date_str = survey_date.strftime('%Y/%m/%d') 
            result.append({'Time' : survey_date_str, 'Area2d' : Area2d})
            
        data_keys = ['Time', 'Area2d']
        
        return self.render_to_csv_response(context=result, data_keys=data_keys)
    
    
class AreaVolumeCalcsViewHTML(TemplateView):
    
    
    template_name = 'surveys/expt.html'
    
    def get(self, request, *args, **kwargs):
        ds_min = 6500
        ds_max = 9000
        # NOTE: will eventually pass in the ds_min/max as request.GET.get('ds_min')
        
        site_id = request.GET.get('site_id')
        site = Site.objects.get(pk=site_id)
        elevationMin = str(site.elevationM(ds_min))
        elevationMax = str(site.elevationM(ds_max))
        #qs = AreaVolume.objects.filter(site_id=site.id).filter(calc_type__iexact='eddy')
        q = QueryDB(SCHEMA_USER, DB_PWD, DB_DESC)
        session = q.create_session()
        distinct_dates = session.query(AreaVolumeCalcBase.calc_date).distinct(AreaVolumeCalcBase.calc_date).filter(func.lower(AreaVolumeCalcBase.calc_type)=='eddy').filter(AreaVolumeCalcBase.site_id==site_id).order_by(AreaVolumeCalcBase.calc_date)
        result = []
        for survey_date in distinct_dates:
            survey_date_str = survey_date.calc_date
            #d1 = qs.filter(calc_date=survey_date).filter(prev_plane_height__lte=elevationMin).filter(next_plane_height__gte=elevationMin).exclude(prev_plane_height__exact='0', plane_height__gte=elevationMin).order_by('plane_height')
            #pickle.dumps(d1)
            d1 = session.query(AreaVolumeCalcBase.plane_height, AreaVolumeCalcBase.next_plane_height, AreaVolumeCalcBase.area_2d_amt).filter(AreaVolumeCalcBase.calc_date==survey_date_str).filter(AreaVolumeCalcBase.next_plane_height>=elevationMin).filter(AreaVolumeCalcBase.prev_plane_height<=elevationMin).filter(AreaVolumeCalcBase.plane_height<elevationMax).filter(AreaVolumeCalcBase.prev_plane_height!=0).order_by(AreaVolumeCalcBase.plane_height)
            d1_list = d1.all()
            if len(d1_list) >= 2:
                plane_height_0 = d1_list[0].plane_height
                plane_height_1 = d1_list[1].plane_height
                area_2d_0 = d1_list[0].area_2d_amt
                area_2d_1 = d1_list[1].area_2d_amt
                minAreaInt = _interpolateCalcs([float(plane_height_0), float(plane_height_1)] , [float(area_2d_0), float(area_2d_1)], float(elevationMin))
                #d2 = qs.filter(calc_date=survey_date).filter(prev_plane_height__lte=elevationMax).filter(next_plane_height__gte=elevationMax).exclude(prev_plane_height__exact='0', plane_height__gte=elevationMax).order_by('plane_height')
                #pickle.dumps(d2)
                d2 = session.query(AreaVolumeCalcBase.plane_height, AreaVolumeCalcBase.next_plane_height, AreaVolumeCalcBase.area_2d_amt).filter(AreaVolumeCalcBase.calc_date==survey_date_str).filter(AreaVolumeCalcBase.next_plane_height>=elevationMax).filter(AreaVolumeCalcBase.prev_plane_height<=elevationMax).filter(AreaVolumeCalcBase.plane_height>=elevationMax).filter(AreaVolumeCalcBase.prev_plane_height!=0).order_by(AreaVolumeCalcBase.plane_height)
                d2_list = d2.all()
                if len(d2_list) >= 2:
                    d2_plane_height_0 = d2_list[0].plane_height
                    d2_plane_height_1 = d2_list[1].plane_height
                    d2_area_2d_amt_0 = d2_list[0].area_2d_amt
                    d2_area_2d_amt_1 = d2_list[1].area_2d_amt
                    maxAreaInt = _interpolateCalcs([float(d2_plane_height_0), float(d2_plane_height_1)] , [float(d2_area_2d_amt_0), float(d2_area_2d_amt_1)], float(elevationMax))
                    Area2d = maxAreaInt - minAreaInt
                else:
                    Area2d = ''
            else:
                Area2d = ''
                
            survey_date_str = survey_date_str
            result.append({'Time' : survey_date_str, 'Area2d' : Area2d})
            
        context = {'result_dict': result}
        
        return self.render_to_response(context=context)
    

                                      
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
    