import json
from django.http import HttpResponse

class JSONResponseMixin(object):
    
    """
    Mixin used to render a JSON response.
    """
    
    def render_to_json_response(self, context, **response_kwargs):
        
        context_json = self.convert_context_to_json(context)
        
        return HttpResponse(context_json, content_type="application/json", **response_kwargs)
    
    def convert_context_to_json(self, context):
        
        json_dump = json.dumps(context)
        
        return json_dump