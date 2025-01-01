from flask import request

class UserRoutes():
    def __init__(self, app, usersController):
        self.app = app
        self.add_routes()
        self.usersController = usersController

    def add_routes(self):
        self.app.add_url_rule('/api/users/login', 'login', self.login, methods=['POST'])
        self.app.add_url_rule('/api/users/signup', 'signup', self.signup, methods=['POST'])
        self.app.add_url_rule('/api/users/signoff', 'signoff', self.signoff, methods=['POST'])
        self.app.add_url_rule('/api/users/refresh_token', 'refresh_token', self.refresh_token, methods=['POST'])

    def login(self):
        return self.usersController.login(request)

    def signup(self):
        return self.usersController.signup(request)
    
    def list_users(self):
        return self.usersController.list_users(request)

    def signoff(self):
        return self.usersController.signoff(request)
    
    def refresh_token(self):
        return self.usersController.refresh_token(request)