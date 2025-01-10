import requests
from requests.exceptions import HTTPError, RequestException
import traceback

class ChatubaApiService:

    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint

    def auth(self, username, password):
        try:
            response = requests.post(  
                f'{self.api_endpoint}/users/login',
                headers= {
                    'Content-Type': 'application/json'
                },
                json={ 'username': username, 'password': password }                        
            )
            response.raise_for_status()
            return response.json()
        except (HTTPError, RequestException) as e:
            return {'error': f'POST /users/logir: {e}'}
        except Exception as e:
            traceback.print_exc()
            print(e)
    
    def signup(self, username, password):
        try:
            response = requests.post(  
                f'{self.api_endpoint}/users/signup',
                headers={
                    'Content-Type': 'application/json'
                },
                json={ 'username': username, 'password': password }                        
            )
            response.raise_for_status()
            return response.json()
        except (HTTPError, RequestException) as e:
            return {'error': f'POST /users/signup : {e}'}
        except Exception as e:
            traceback.print_exc()
            print(e)
            
    def list_available_group_chats(self, token):
        try:
            response = requests.get(  
                f'{self.api_endpoint}/chats',
                headers={
                    'Authorization': f'Bearer {token}'
                },                   
            )
            response.raise_for_status()
            return response.json()
        except (HTTPError, RequestException) as e:
            return {'error': f'GET /chats: {e}'}
        except Exception as e:
            traceback.print_exc()
            print(e)

    def list_available_users(self, token):
        pass

    def create_chat(self, token, chatname):
        try:
            response = requests.post(  
                f'{self.api_endpoint}/chats',
                headers={'Authorization': f'Bearer {token}'},                   
                json={'chat_name': chatname}
            )
            response.raise_for_status()
            return response.json()
        except (HTTPError, RequestException) as e:
            return {'error': f'POST /chats: {e}'}
        except Exception as e:
            traceback.print_exc()
            print(e)
