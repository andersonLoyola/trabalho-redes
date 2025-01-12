import requests
import traceback
from requests.exceptions import HTTPError, RequestException
import urllib3

class AuthService:

    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def signin(self, username, password):
        try:
            response = requests.post(  
                f'{self.api_endpoint}/users/login',
                headers= {
                    'Content-Type': 'application/json'
                },
                json={ 'username': username, 'password': password },
                verify=False   #as the ssl certificate is currently self-signed it won't be truted             
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
                json={ 'username': username, 'password': password },
                verify=False   #as the ssl certificate is currently self-signed it won't be truted                                     
            )
            response.raise_for_status()
            return response.json()
        except (HTTPError, RequestException) as e:
            return {'error': f'POST /users/signup : {e}'}
        except Exception as e:
            traceback.print_exc()
            print(e)
    
    def signoff(self, user_id, session_id, token):
        try:
            response = requests.post(  
                f'{self.api_endpoint}/users/signoff',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'
                },
                json={ 'user_id': user_id, 'session_id': session_id },
                verify=False   #as the ssl certificate is currently self-signed it won't be truted                                     
            )
            response.raise_for_status()
            return response.json()
        except (HTTPError, RequestException) as e:
            return {'error': f'POST /users/signup : {e}'}
        except Exception as e:
            traceback.print_exc()
            print(e)
            
  

   
   
