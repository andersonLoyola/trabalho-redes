from flask import request

class UserRoutes():
    def __init__(self, app, usersController):
        self.app = app
        self.add_routes()
        self.usersController = usersController

    def add_routes(self):
        self.app.add_url_rule('/api/login', 'login', self.login, methods=['POST'])
        self.app.add_url_rule('/api/signup', 'signup', self.signup, methods=['POST'])
        self.app.add_url_rule('/api/signoff', 'signoff', self.signoff, methods=['POST'])
        self.app.add_url_rule('/api/refresh_token', 'refresh_token', self.refresh_token, methods=['POST'])

    def login(self):
        return self.usersController.login(request.json)

    def signup(self):
        return self.usersController.signup(request.json)

    def signoff(self):
        return self.usersController.signoff(request.json)
    
    def refresh_token(self):
        return self.usersController.refresh_token(request.json)