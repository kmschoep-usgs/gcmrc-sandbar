from django.conf.urls import patterns, url

from djangojs.views import JasmineView

class ProjectJasmineView(JasmineView):
    
    template_name = 'jasmine_test_runner.html'
    js_files = (
        'js/SiteMarker.js',
        'js/DateRange.js',
        'js/tests/*.spec.js'
    )
    
urlpatterns = patterns('',
    url(r'^jasmine/$', 
        ProjectJasmineView.as_view(),
        name='project_jasmine_js_tests'),                
)