
from django.conf import settings
from django.conf.urls import patterns, url, include
from common.views import SandbarHome

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^home/$',
        SandbarHome.as_view(),
        name='home'),
    url(r'^surveys/', include('surveys.urls')),
 
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^area_vol_calc/$', 'flatpage', {'url' : '/area_vol_calc/'}, name='area_vol_calc'));

