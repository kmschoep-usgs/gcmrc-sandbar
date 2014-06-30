import logging
import mimetypes
from urllib2 import urlopen, HTTPError

from django.http import HttpResponse
from django.views.generic import View, TemplateView

logger = logging.getLogger(__name__)

class SimpleWebServiceProxyView(View):
    
    service_url = '' # Web service url ending in slash
    
    def get(self, request, *args, **kwargs):
        if  'op' in kwargs:
            kwargs['op'] = kwargs['op'] + '/'
        else:
            kwargs['op'] = '';
        target_url = '%s%s?%s' % (self.service_url, kwargs['op'], request.META.get('QUERY_STRING', ''))
        
        logger.debug('Proxy url is ' + target_url)
        
        try:
            proxied_request = urlopen(target_url)
            status_code = proxied_request.code
            content_type = proxied_request.headers.typeheader or mimetypes.guess_type(target_url)
            content = proxied_request.read()
        except HTTPError as e:
            logger.debug('Can\'t complete request to ' + target_url)
            return HttpResponse(e.msg, status=e.code, content_type='text/plain')
        else:
            return HttpResponse(content, status=status_code, content_type=content_type)
        
        
class SandbarHome(TemplateView):
    
    template_name = 'home.html'
    
    def get(self, request, *args, **kwargs):
        
        context = None
        
        return self.render_to_response(context) 