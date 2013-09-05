
from django.conf.urls import patterns, url

from .views import SitesView

urlpatterns = patterns('',
    url(r'^sites/$',
        SitesView.as_view(),
        name='surveys-sites')
)