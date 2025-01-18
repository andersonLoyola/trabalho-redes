import json
import urllib3
import requests
import traceback
from serializers import CryptoSerializer
from requests.exceptions import HTTPError, RequestException

class AuthService:

    api_endpoint: str
    api_key: str
    crypto_serializer: CryptoSerializer

    def __init__(self, api_endpoint: str, api_key: str, crypto_serializer: CryptoSerializer):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.crypto_serializer = crypto_serializer
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def signin(self, username: str, password: str):
        try:
            encrypted_request_body = self.crypto_serializer.encrypt(json.dumps({ 
                'username': username, 
                'password': password 
            }).encode('utf-8'))
            response = requests.post(  
                f'{self.api_endpoint}/users/login',
                headers= {
                    'Content-Type': 'application/json',
                    'x-client-id': 'cmd-client',
                    'x-api-key': self.api_key
                },
                json=encrypted_request_body,
                verify=False   #as the ssl certificate is currently self-signed it won't be trusted             
            )
            response.raise_for_status()
            return response.json()
        except (HTTPError, RequestException) as e:
            return {'error': f'POST /users/login: {e}'}
        except Exception as e:
            traceback.print_exc()
            print(str(e))
    
    def signup(self, username: str, password: str):
        try:
            encrypted_request_body = self.crypto_serializer.encrypt(json.dumps({ 
                'username': username, 
                'password': password 
            }).encode('utf-8'))
            response = requests.post(  
                f'{self.api_endpoint}/users/signup',
                headers={
                    'Content-Type': 'application/json',
                    'x-client-id': 'cmd-client',
                    'x-api-key': self.api_key
                },
                json=encrypted_request_body,
                verify=False   #as the ssl certificate is currently self-signed it won't be truted                                     
            )
            response.raise_for_status()
            return response.json()
        except (HTTPError, RequestException) as e:
            return {'error': f'POST /users/signup : {e}'}
        except Exception as e:
            traceback.print_exc()
            print(str(e))
    
    def signoff(self, user_id: str, session_id: str):
        try:
            encrypted_request_body = self.crypto_serializer.encrypt(json.dumps(
                { 
                    'user_id': user_id, 
                    'session_id': session_id 
                    }
                ).encode('utf-8')
            )
            response = requests.post(  
                f'{self.api_endpoint}/users/signoff',
                headers={
                    'Content-Type': 'application/json',
                    'x-api-key': self.api_key,
                    'x-client-id': 'cmd-client'
                },
                json=encrypted_request_body,
                verify=False   #as the ssl certificate is currently self-signed it won't be truted                                     
            )
            response.raise_for_status()
            return response.json()
        except (HTTPError, RequestException) as e:
            return {'error': f'POST /users/signup : {e}'}
        except Exception as e:
            traceback.print_exc()
            print(str(e))
            
  

   
   
