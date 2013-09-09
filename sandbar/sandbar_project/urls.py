
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from jasmine.test_urls import ProjectJasmineView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^home/$',
        TemplateView.as_view(template_name='home.html'),
        name='home'),
    url(r'^surveys/', include('surveys.urls')),
                       
    url(r'^djangojs/', include('djangojs.urls')),
 
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if 'jasmine' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', url(r'^jasmine/$', ProjectJasmineView.as_view()))
