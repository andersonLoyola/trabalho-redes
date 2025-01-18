import json

class HTTPRequestSerializer(): 

    def _parse_headers(self, request):
        header = {}
        for name, value in request.headers.items():
            header[name] = value
        return header
   
    def _parse_query_params(self, query_str):
        if (len(query_str) == 0):
            return {}
        query = {}
        query_params = query_str.split('&')
        for param in query_params:
            key, value = param.split('=')
            query[key] = value
        return query
   
    def _parse_body(self, request):
        content_length = request.headers.get("content-length")
        content_type = request.headers.get('content-type') 
        if not content_length or int(content_length) == 0:
            return {}
        length = int(content_length)
        rfile_str = request.rfile.read(length).decode("utf8") #AKA BODY STRING
        if content_type != 'application/json':
            return rfile_str
        return json.loads(rfile_str)
   
   
    # @IMPORTANT: api urls must follow /api/v1/<resource>/<identifier />
    def rest_path_parser(self, path):
        entries = path.split('/')
        return {
            'version': entries[2],
            'resource': entries[3],

        }


    def parse_request(self, request):
        # CAUSE THERES NO FING NULL SAFETTY OPERATOR IS THIN FKIN  LANGUAGE
        if '?' in request.path:
            path, query_str = request.path.split('?')
            query = self._parse_query_params(query_str)
        else:
            path = request.path
            query = {}
        api_info = self.rest_path_parser(path)
        body = self._parse_body(request)
        headers = self._parse_headers(request)
        method = request.command
        
        return {
            'resource': api_info['resource'],
            'headers': headers,
            'method': method,
            'query': query,
            'path': path,
            'body':body,
        }

