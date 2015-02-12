'''
Created on Feb 12, 2015

@author: kmschoep
'''
from django.conf import settings

def project_settings(request):
    ''' 
    Returns a dictionary with a settings key which contains the dictionary of
    settings that will be available in the context variable settings
    '''
    
    # Specify which settings you want exposed.
    exposed_settings = ('GA_TRACKING_CODE',)
    settings_dict = dict((key, getattr(settings, key)) if hasattr(settings, key) else (key, '') for key in exposed_settings)
    
    return {'settings': settings_dict}