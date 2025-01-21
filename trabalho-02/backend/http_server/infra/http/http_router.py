import re

class HTTPRouter(): 
    routes = {}
    handlers = {}

    def match_route(self, routes, path):
        for route, handler_name in routes.items():
            pattern = re.sub(r'<[^/]+>', r'([^/]+)', route)
            match = re.match(f'^{pattern}$', path, re.IGNORECASE)
            if match:
                return handler_name, match.groups()
        return None, None

 
    
    def add_url_rule(self, name, path, handler_name, handler, method):
        if method not in self.routes:
            self.routes[method] = {}
        self.routes[method][path] = handler_name

        if name not in self.handlers:
            self.handlers[name] = {}
        self.handlers[name][handler_name] = handler

    
    def route_request(self, parsed_request):
        resource = parsed_request['resource']
        method = parsed_request['method']
        path = parsed_request['path']
        handler_name, params = self.match_route(self.routes.get(method, {}), path)

        if not handler_name or not resource:
            return None

        return self.handlers[resource][handler_name](parsed_request, *params)


    def get_supported_methods(self): 
        supported_methods = [
            method
            for method in self.routes 
        ]
        
        return ', '.join(supported_methods)
 
    def get_available_routes(self):
        pass
