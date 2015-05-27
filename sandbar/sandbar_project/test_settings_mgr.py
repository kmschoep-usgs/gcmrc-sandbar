'''
Created on May 27, 2015

@author: kmschoep
'''
from django.conf import settings
from django.core.management import call_command
from django.db.models import loading

NO_SETTING = ('!', None)

class TestSettingsManager(object):
    """
    A class which can modify some Django settings temporarily for a
    test and then revert them to their original values later.

    Automatically handles resyncing the DB if INSTALLED_APPS is
    modified.
    
    This code came from http://djangosnippets.org/snippets/1011/

    """
    def __init__(self):
        self._original_settings = {}

    def set(self, **kwargs):
        for k,v in kwargs.iteritems():
            self._original_settings.setdefault(k, getattr(settings, k,
                                                          NO_SETTING))
            setattr(settings, k, v)
        if 'INSTALLED_APPS' in kwargs:
            self.syncdb()

    def syncdb(self):
        loading.cache.loaded = False
        call_command('migrate', verbosity=0)

    def revert(self):
        for k,v in self._original_settings.iteritems():
            if v == NO_SETTING:
                delattr(settings, k)
            else:
                setattr(settings, k, v)
        if 'INSTALLED_APPS' in self._original_settings:
            self.syncdb()
        self._original_settings = {}