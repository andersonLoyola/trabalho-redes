import os
import getpass
class AuthHandler:

    def __init__(self, api_service):
        self.api_service = api_service
    
        
    def handle_login(self):
        while True:
            os.system('cls')
            print('type \\q to quit')
            username = str(input('Enter username: '))
            if username == '\\q':
                return
            password = getpass.getpass("Enter your password: ")
            response = self.api_service.signin(username, password)
            if 'error' not in response:
                os.system('cls')
                return response['token']
            else:
                input(f'{response['error']}')

    def handle_signup(self):
        while True:
            os.system('cls')
            print('type \\q to quit')
            username = input('Enter username: ')
            if username == '\\q':
                return
            password = getpass.getpass('Enter your password: ')
            response = self.api_service.signup(username, password)
            if 'error' not in response:
                os.system('cls')
                return response
            else:
                input(f'{response['error']}')