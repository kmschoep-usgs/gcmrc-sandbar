from django.conf.urls import patterns, url

from djangojs.views import JasmineView

class ProjectJasmineView(JasmineView):
    
    template_name = 'jasmine_test_runner.html'
    js_files = (
        'js/SiteMarker.js',
        'js/DateRange.js',
        'js/GDAWSService.js',
        'js/GDAWSFormatUtils.js',
        'js/SitePlots.js',
        'js/tests/lib/sinon-1.7.3.js',
        'js/tests/*.spec.js'
    )
    
urlpatterns = patterns('',
    url(r'^jasmine/$', 
        ProjectJasmineView.as_view(),
        name='project_jasmine_js_tests'),                
)