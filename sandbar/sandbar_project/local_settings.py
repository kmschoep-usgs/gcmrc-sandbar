'''
Created on Aug 29, 2013

@author: kmschoep
'''
from sys import argv
import os
PROJECT_HOME = os.path.dirname(__file__)
SITE_HOME = os.path.split(PROJECT_HOME)[0]
DEBUG = True
#TEMPLATE_DEBUG = DEBUG
#SOUTH_LOGGING_FILE = os.path.join(os.path.dirname(__file__),"south.log")
#SOUTH_LOGGING_ON = True

SCHEMA_USER = 'sandbar'
DB_PWD = '<password>'
DB_NAME = 'DBDW.ER.USGS.GOV'

DJANGOTEST_PWD = '<password>'


# This checks to see if django tests are running (i.e. manage.py test)
if argv and 1 < len(argv):
    RUNNING_TESTS = 'test' in argv
else:
    RUNNING_TESTS= False

if not RUNNING_TESTS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.oracle', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'cida-eros-dbdw.er.usgs.gov:1521/dbdw.er.usgs.gov',  # Or path to database file if using sqlite3.
            'USER': 'sandbar_user',                     # Not used with sqlite3.
            'PASSWORD': '<password>',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        },
        'sandbar': {
            'ENGINE': 'django.contrib.gis.db.backends.oracle', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': DB_NAME,                      # Or path to database file if using sqlite3.
            'USER': SCHEMA_USER,                     # Not used with sqlite3.
            'PASSWORD': DB_PWD,                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

POSTGIS_VERSION = (2, 1, 1)

STATIC_URL = '/static/'

GDAWS_SERVICE_URL = 'http://cida-eros-gcmrcdev.er.usgs.gov:8080/gcmrc-services/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '<secret-key>'