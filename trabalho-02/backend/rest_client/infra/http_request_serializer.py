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
    """
        TODO: notice that we are currently not handling cases where the content length is set a s
        "0", a typical case is when we do a POST request from postman withOUT A body
    """       
    def _parse_body(self, request):
        content_length = request.headers.get("content-length")
        if (content_length):
            length = int(content_length)
            rfile_str = request.rfile.read(length).decode("utf8") #AKA BODY STRING
            return json.loads(rfile_str)
        return {}
   
    # TODO: see better eay to do it later
    # @IMPORTANT: api urls must follow /api/v1/resource/<identifier />
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

