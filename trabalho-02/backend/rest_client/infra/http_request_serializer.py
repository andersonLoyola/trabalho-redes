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
        length = int(request.headers.get("content-length"))
        rfile_str = request.rfile.read(length).decode("utf8") #AKA BODY STRING
        return json.loads(rfile_str)
   
    # TODO: see better eay to do it later
    def rest_path_parser(self, path):
        (_,_, api_version, api_resource) = path.split('/')
        return {
            'version': api_version,
            'resource': api_resource,
 
        }


    def parse_request(self, request):
        path, query_str = request.path.split('?')
        api_info = self.rest_path_parser(path)
        body = self._parse_body(request)
        headers = self._parse_headers(request)
        query = self._parse_query_params(query_str)
        method = request.command
        
        return {
            'resource': api_info['resource'],
            'headers': headers,
            'method': method,
            'query': query,
            'path': path,
            'body':body,
        }

