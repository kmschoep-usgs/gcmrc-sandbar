from django.db import models
from django.conf import settings
'''
Created on Aug 29, 2013

@author: kmschoep
'''
class SandbarRouter(object):
    """
    A router to control all database operations on models in the
    sandbar application.
    """
    def allow_syncdb(self, db, model):
        """
        Make sure the south app only appears in the 'sandbar'
        database.
        """
        if db == 'sandbar':
            return model._meta.app_label == 'southtut'
        elif model._meta.app_label == 'southtut':
            return False
        return None