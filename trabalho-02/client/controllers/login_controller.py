import requests

class LoginController:
    def __init__(self, chatuba_enpoint_url, on_login):
        self.url = chatuba_enpoint_url
        self.on_login = on_login

    def login(self, username, password):
        data = {
            'username': username,
            'password': password
        }
        response = requests.post(f'{self.url}/login', json=data)
        if response.status_code == 200:
            self.on_login(response.json())
        # print("Login failed")