import json
import csv

from django.http import HttpResponse
        

class CSVResponseMixin(object):
    
    """
    Mixin used to create a CSV response.
    """
    
    def render_to_csv_response(self, context, data_keys=None, download=False, download_name=None, **response_kwargs):
        
        response = HttpResponse(content_type='text/csv')
        if download:
            if download_name:
                content_disposition = 'attachment; filename="{download_name}.csv"'.format(download_name=download_name)
                response['Content-Disposition'] = content_disposition
            else:
                response['Content-Disposition'] = 'attachment; filename="areavolumedata.csv"'
        self._write_csv_content(data=context, outfile=response, data_keys=data_keys)
        
        return response
         
    def _write_csv_content(self, data, outfile, data_keys=None):
        
        if data_keys == None:
            data_keys = data[0].keys()
        else:
            data_keys = data_keys
        csv_writer = csv.DictWriter(outfile, delimiter=',', fieldnames=data_keys)
        csv_writer.writerow(dict((data_key, data_key) for data_key in data_keys))
        for data_dict in data:
            csv_writer.writerow(data_dict)
        

class JSONResponseMixin(object):
    
    """
    Mixin used to render a JSON response.
    """
    
    def render_to_json_response(self, context, **response_kwargs):
        
        context_json = self._convert_context_to_json(context)
        
        return HttpResponse(context_json, content_type="application/json", **response_kwargs)
        
    def _convert_context_to_json(self, context):
        
        json_dump = json.dumps(context)
        
        return json_dump