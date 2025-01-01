

class UserRoutes():
    def __init__(self, http_router, usersController):
        self.http_router = http_router
        self.add_routes()
        self.usersController = usersController

    def add_routes(self):
        self.http_router.add_url_rule('users','/api/v1/users/login', 'login', self.login, 'POST')
        self.http_router.add_url_rule('users','/api/v1/users/signup', 'signup', self.signup, 'POST')
        self.http_router.add_url_rule('users','/api/v1/users/signoff', 'signoff', self.signoff, 'POST')
        self.http_router.add_url_rule('users','/api/v1/users/refresh_token', 'refresh_token', self.refresh_token, 'POST')

    def login(self, request):
        return self.usersController.login(request)

    def signup(self, request):
        return self.usersController.signup(request)
    
    def list_users(self, request):
        return self.usersController.list_users(request)

    def signoff(self, request):
        return self.usersController.signoff(request)
    
    def refresh_token(self, request):
        return self.usersController.refresh_token(request)