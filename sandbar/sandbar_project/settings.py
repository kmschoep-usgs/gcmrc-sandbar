# Django settings for sandbar project.
from sys import argv
import os
#from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

try:
    from local_settings import DJANGOTEST_PWD
except ImportError:
    DJANGOTEST_PWD = ''

PROJECT_HOME = os.path.dirname(__file__)
SITE_HOME = os.path.split(PROJECT_HOME)[0]

DEBUG = False
#TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Mary Bucknell', 'mbucknell@usgs.gov'),
     ('Andrew Yan', 'ayan@usgs.gov'),
     ('Kathryn Schoepoester', 'kmschoep@usgs.gov'),
)

MANAGERS = ADMINS

# This checks to see if django tests are running (i.e. manage.py test)
if argv and 1 < len(argv):  
    RUNNING_TESTS = 'test' in argv
else:  
    RUNNING_TESTS = False  

if RUNNING_TESTS:
    DATABASES = { 
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'test_geodjango_db',                      # Or path to database file if using sqlite3.
            'USER': 'djangotest',                     # Not used with sqlite3.
            'PASSWORD': DJANGOTEST_PWD,                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }    

else:
    # Default engine. Should be overridden in local_settings.py to connect to sandbar databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.path.join(SITE_HOME, 'sqlite.db'),                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': '',
            'PASSWORD': '',
            'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        }
    }

#DATABASE_ROUTERS = ['routers.SandbarRouter']

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

#TEST_RUNNER = 'sandbar_project.test_runner.ManagedModelTestRunner'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(SITE_HOME, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    (os.path.join(PROJECT_HOME, 'static'),)
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

#TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
#                               "django.core.context_processors.debug",
#                               "django.core.context_processors.i18n",
#                               "django.core.context_processors.media",
#                               "django.core.context_processors.static",
#                               "django.core.context_processors.tz",
#                               "django.contrib.messages.context_processors.messages",
#                               "common.context_processors.project_settings",
#                               )
#
# List of callables that know how to import templates from various sources.
#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
#)

TEMPLATES = [
    {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                os.path.join(PROJECT_HOME, 'templates'),
                 os.path.join(PROJECT_HOME, 'templates/surveys'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'common.context_processors.project_settings',
            ],
            'debug': [
                      DEBUG,
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
#    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'sandbar_project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'sandbar_project.wsgi.application'

#TEMPLATE_DIRS = (
#    os.path.join(PROJECT_HOME, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
#    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
#    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    #Third party apps
    #CIDA apps
    'surveys',
    'common',
)

#SOUTH_TESTS_MIGRATE = False
# SOUTH_DATABASE_ADAPTERS = {'default':'south.db.oracle', 'sandbar':'south.db.oracle'} 

LOG_FILE_DIR = os.getenv('HOME', '') + '/logs/sandbar/'
if not os.path.exists(LOG_FILE_DIR):
    LOG_FILE_DIR = SITE_HOME + '/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard' : {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        }
    },

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true' : {
            '()' : 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
           'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_DIR + 'sandbar.log',
            'maxBytes': 1024000,
            'backupCount': 10,
            'formatter': 'standard'                 
        },
       'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'  
        }               
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins','file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'common': {
            'handlers': ['file'],
            'level' : 'DEBUG',
            'propagate' : True,
            'filters' : ['require_debug_false']
        },
        'surveys': {
            'handlers': ['file'],
            'level' : 'DEBUG',
            'propagate' : True,
            'filters' : ['require_debug_false']
        },                

    }
}

# Code to be used for google analytics. If tracking is desired for a server, set to the track code in local_settings.py.
GA_TRACKING_CODE = ''

GDAWS_SERVICE_URL = 'http://www.gcmrc.gov/discharge_qw_sediment/services/'

LOCAL_LOGGERS = None
LOCAL_APPS = None

try:
    from local_settings import *
except ImportError:
    # add apps to this variable for this specific server configuration
    pass

if LOCAL_LOGGERS:
    LOGGING['loggers'].update(LOCAL_LOGGERS)

if LOCAL_APPS:
    INSTALLED_APPS += LOCAL_APPS

if os.getenv('JENKINS_URL', False):
    #SOUTH_DATABASE_ADAPTERS = {'default':'south.db.postgresql_psycopg2'}
    POSTGIS_VERSION = (2, 1, 1) # Googling suggests that Django has a hard time reading the settings for Postgres 9.3 and PostGIS 2.1
    JENKINS_TASKS = ('django_jenkins.tasks.run_pylint',
                     'django_jenkins.tasks.with_coverage',) # This is where you would add other django_jenkins tasks
#    JENKINS_TEST_RUNNER = '' # If you need to define your own test runner for jenkins do it here
    INSTALLED_APPS += ('django_jenkins', 
                       'jasmine',
                       )
    PROJECT_APPS = ('common', 
                    'surveys', 
                    'jasmine',
                    ) # This is where you would add the apps that you would like tested
    DATABASES['default'].update(dict(
          ENGINE = os.getenv('DBA_SQL_DJANGO_ENGINE'),
          NAME = os.getenv('DBA_SQL_DB_NAME'),
          USER = os.getenv('DBA_SQL_ADMIN'),
          PASSWORD = os.getenv('DBA_SQL_ADMIN_PASSWORD'),
          HOST = os.getenv('DBA_SQL_HOST'),
          PORT = os.getenv('DBA_SQL_PORT')
    )) # This allows you to define your database to be used for tests using environment variables

