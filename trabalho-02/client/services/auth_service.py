import requests


class AuthService():

    def __init__(self, url):
        self.url = url

    def login(self, username, password):
        try:
            response = requests.post(
                f'{self.url}/login',
                json={'username': username, 'password': password}
            )
            return response.json()
        except Exception as e:
            print(e)
            return {'error': str(e)}

    def register(self, username, password):
        try: 
            response = requests.post(
                f'{self.url}/register',
                json={'username': username, 'password': password}
            )
            return response.json()
        except Exception as e:
            print(e)
            return {'error': str(e)}