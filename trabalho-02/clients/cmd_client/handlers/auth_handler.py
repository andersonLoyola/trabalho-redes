import os
import getpass
class AuthHandler:

    def __init__(self, api_service):
        self.api_service = api_service
    
    def _login_request(self):
        os.system('cls')
        username = str(input('Enter username: '))
        password = getpass.getpass("Enter your password: ")
        response = self.api_service.signin(username, password)
        return response
        
    def _sign_up_request(self):
        os.system('cls')
        username = input('Enter username: ')
        password = getpass.getpass('Enter your password: ')
        response = self.api_service.signup(username, password)
        return response
        
    """
        TODO:
        Currently there is no way to break free form this, i think we
        should implement a option to left this whenever want
    """ 
    def handle_login(self):
        while True:
            response = self._login_request()
            if 'error' not in response:
                os.system('cls')
                return response['token']
            else:
                print(f'{response['error']}')

    def handle_signup(self):
        while True:
            response = self._sign_up_request()
            if 'error' not in response:
                os.system('cls')
                return response
            else:
                input(f'{response['error']}')