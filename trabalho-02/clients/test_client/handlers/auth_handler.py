import os

class AuthHandler:

    def __init__(self, conn, msg_service):
        self.conn = conn
        self.msg_service = msg_service
    
    def _login_request(self):
        os.system('cls')
        username = str(input('Enter username: '))
        password = str(input('Enter password: '))
        message = {
            "request_type": "auth", 
            "username": username, 
            "password": password
        }
        self.msg_service.send_message(self.conn, message)

    def _sign_up_request(self):
        os.system('cls')
        username = input('Enter username: ')
        password = input('Enter password: ')
        message = {
            "request_type": "signup", 
            "username": username, 
            "password": password
        }
        self.msg_service.send_message(self.conn, message)
        

    def handle_login(self):
        self._login_request()
        while True:
            response = self.msg_service.receive_message(self.conn)
            if not response:
                continue
            if 'success' in response and response['response_type'] == 'auth':
                os.system('cls')
                return response
            elif response and 'error' in response:
                print(response['error'])
                self._login_request()

    def handle_signup(self):
        self._sign_up_request()
        while True:
            response = self.msg_service.receive_message(self.conn)
            if not response:
                continue
            if 'success' in response and response['response_type'] == 'signup':
                os.system('cls')
                return response
            elif response and 'error' in response:
                input(response['error'])
                self._sign_up_request()