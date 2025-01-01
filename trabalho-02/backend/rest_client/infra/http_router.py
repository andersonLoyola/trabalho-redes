"""
    IDK IF TI IS THE BEST WAY TO DO IT:
    THE IDEA IS TO MAKE THIS SHIT WORK ROUTING THE REQUEST TO THE REGISTERED ROUTES
"""
import re

class HTTPRouter(): 
    routes = {
        'GET': {},
        'POST': {},
        'DELETE': {},
        'PATCH': {},
    }

    handlers = {}

    """
        TODO: rewrite this shit later
        IT BASICALLY APPLIES REGEX RULE TO KNOW IF THE ROUTE IS 
        SUPPORTED BY THE SERVER
        MAYBE THIS SHIT IS SLOW AF, BUT IDK, IT ISTHE ONLY WAY I FIGUREOUT HOW  TO 
        DO IT
    """
    def match_route(self, routes, path):
        for route, handler in routes.items():
            pattern = re.sub(r'<[^/]+>', r'([^/]+)', route)
            match = re.match(f'^{pattern}$', path, re.IGNORECASE)
            if match:
                return handler
        return None
 
    # MAYBE INFER FROM RESOURCE_NAME FORM PATH LATER
    def add_url_rule(self, name, path, handler_name, method, handler):
        self.routes[method][path] = handler_name
        if name not in self.handlers:
            self.handlers[name] = {
                handler_name: handler
            }
        else: 
            self.handlers[name][handler_name] = handler
    
    def route_request(self, parsed_request): 
        resource = parsed_request['resource']
        method = parsed_request['method']
        path = parsed_request['path']
        handler_name = self.match_route(self.routes[method], path)

        if not handler_name or not resource:
            return None
        
        return self.handlers[resource][handler_name](parsed_request)
