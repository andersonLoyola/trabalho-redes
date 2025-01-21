class UserRoutes():
    def __init__(self, http_router, users_controller):
        self.http_router = http_router
        self.add_routes()
        self.users_controller = users_controller

    def add_routes(self):
        self.http_router.add_url_rule('users','/api/v1/users/login', 'login', self.login, 'POST')
        self.http_router.add_url_rule('users','/api/v1/users/signup', 'signup', self.signup, 'POST')
        self.http_router.add_url_rule('users','/api/v1/users/signoff', 'signoff', self.signoff, 'POST')

    def login(self, request):
        return self.users_controller.login(request)

    def signup(self, request):
        return self.users_controller.signup(request)
    
    def signoff(self, request):
        return self.users_controller.signoff(request)
    
   