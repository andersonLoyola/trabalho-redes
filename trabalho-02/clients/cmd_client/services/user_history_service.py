import json
import urllib3
import requests
import traceback
from serializers import CryptoSerializer
from requests.exceptions import HTTPError, RequestException

class UserHistoryService:

    api_endpoint: str
    api_key: str
    crypto_serializer: CryptoSerializer

    def __init__(self, api_endpoint: str, api_key: str, crypto_serializer: CryptoSerializer):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.crypto_serializer = crypto_serializer
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_group_chat_messages_from_chat(self, user_id: str, chat_name: str):
        try:
            encrypted_request_body = self.crypto_serializer.encrypt(json.dumps({ 
                'user_id': user_id, 
                'chat_name': chat_name 
            }).encode('utf-8'))
            response = requests.get(
                f'{self.api_endpoint}/messages/group-messages',
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
            return {'error': f'GET /chats/group-messages: {str(e)}'}
        except Exception as e:
            traceback.print_exc()
            print(str(e))
    

  

   
   
