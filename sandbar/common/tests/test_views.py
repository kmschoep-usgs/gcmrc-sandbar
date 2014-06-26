
import mock

from urllib2 import HTTPError

from django.test import TestCase, SimpleTestCase
from django.test.client import RequestFactory, Client
from django.core.urlresolvers import reverse


from ..views import SimpleWebServiceProxyView

class SimpleWebServiceProxyViewTestCase(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        
        self.test_view = SimpleWebServiceProxyView(service_url="http://www.fake.com/service/")
        
    def test_get_success_no_op(self):
        with mock.patch('common.views.urlopen') as mock_urlopen:
            proxied_request = mock.Mock()
            proxied_request.code = 200
            proxied_request.read.return_value = 'This content'
            mock_header = mock.Mock()
            mock_header.typeheader = 'image/png'
            proxied_request.headers = mock_header
            mock_urlopen.return_value = proxied_request
                
            request = self.factory.get('/my_service/?param=1&param=2')        
            response = self.test_view.get(request)
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, 'This content')
            self.assertEqual(response['Content-Type'], 'image/png')
            
            self.assertEqual(mock_urlopen.call_args[0], ('http://www.fake.com/service/?param=1&param=2',))
   
    def test_get_success_op(self):
        with mock.patch('common.views.urlopen') as mock_urlopen:
            proxied_request = mock.Mock()
            proxied_request.code = 200
            proxied_request.read.return_value = 'This content'
            mock_header = mock.Mock()
            mock_header.typeheader = 'image/png'
            proxied_request.headers = mock_header
            mock_urlopen.return_value = proxied_request
            args = []
            kwargs = {'op' : 'specific_op'}
                
            request = self.factory.get('/my_service/specfic_op/?param=1&param=2')        
            response = self.test_view.get(request, *args, **kwargs)
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, 'This content')
            self.assertEqual(response['Content-Type'], 'image/png')
            
            self.assertEqual(mock_urlopen.call_args[0], ('http://www.fake.com/service/specific_op/?param=1&param=2',))

    def test_get_failure(self):
        with mock.patch('common.views.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = HTTPError('http://www.fake.com/service/?param=1&param=2', 404, 'Can not find service', {}, None)
            
            request = self.factory.get('/my_service/?param=1&param=2')        
            response = self.test_view.get(request)
            
            self.assertEqual(response['Content-Type'], 'text/plain')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.content,'Can not find service')

class TestSandbarHomeView(SimpleTestCase):
    
    def setUp(self):
        
        self.c = Client()
        
    def test_view_response(self):
        
        response = self.c.get(reverse('home'))
        resp_status_code = response.status_code
        expected_status_code = 200
        self.assertEqual(resp_status_code, expected_status_code)