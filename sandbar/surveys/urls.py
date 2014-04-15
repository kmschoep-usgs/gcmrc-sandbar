
from django.conf.urls import patterns, url

from .views import SitesListView, SiteDetailView, GDAWSWebServiceProxy, AreaVolumeCalcsView, DygraphView

urlpatterns = patterns('',
    url(r'^sites/$',
        SitesListView.as_view(),
        name='surveys-site_list'),
    url(r'^site/(?P<pk>\d+)/$',
        SiteDetailView.as_view(),
        name='surveys-site'),
    url(r'^gdaws/(?P<op>[A-Za-z0-9-_/]*)/$',
        GDAWSWebServiceProxy.as_view(),
        name='surveys-gdaws'),
    url(r'^areavolume',
        AreaVolumeCalcsView.as_view(),
        name='surveys-areavolume'),
    url(r'^dygraph_page',
        DygraphView.as_view(),
        name='dygraphs_page'),                 
)