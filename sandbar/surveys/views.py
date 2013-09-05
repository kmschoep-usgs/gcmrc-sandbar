
from django.db.models import Min, Max
from django.views.generic import ListView

from .models import Site, Survey

class SitesView(ListView):
    '''
    Extends ListView to serve site data including the min and max survey date. 
    '''
    
    template_name = 'surveys/sites.html'
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
