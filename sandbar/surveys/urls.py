
from django.conf.urls import patterns, url

import views as sb_vw

urlpatterns = patterns('',
    url(r'^sites/$',
        sb_vw.SitesListView.as_view(),
        name='surveys-site_list'),
    url(r'^site/(?P<pk>\d+)/$',
        sb_vw.SiteDetailView.as_view(),
        name='surveys-site'),
    url(r'^gdaws/(?P<op>[A-Za-z0-9-_/]*)/$',
        sb_vw.GDAWSWebServiceProxy.as_view(),
        name='surveys-gdaws'),
    url(r'^areavolume',
        sb_vw.AreaVolumeCalcsView.as_view(),
        name='surveys-areavolume'),  
    url(r'^sites_geo_json/$',
        sb_vw.SandBarSitesGeoJSON.as_view(),
        name="gjson_sites"),
    url(r'^site_area_info',
        sb_vw.BasicSiteInfoJSON.as_view(),
        name='basic_area_info'),
    url(r'^expt',
        sb_vw.AreaVolumeCalcsTemp.as_view(),
        name='expt'),
    url(r'^datadownload',
        sb_vw.AreaVolumeCalcsDownloadView.as_view(),
        name='data_download'),                 
)