import urllib3
import requests

class RestService:

    api_host=''
    api_key=''
  
    def __init__(self, api_host: str, api_key):
        self.api_host = api_host
        self.api_key = api_key
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def store_group_message_request(self, data):
        response = requests.post(
            f'{self.api_host}/messages/group-messages',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': self.api_key,
                'x-client-id': 'websocket-server'   
            },
            json=data,
            verify=False
        )
        response.raise_for_status()
        return response.json()
      
    def store_private_message_request(self, data):
        response = requests.post(
            f'{self.api_host}/messages/private-messages',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': self.api_key,
                'x-client-id': 'websocket-server'   
            },
            json=data,
            verify=False
        )
        response.raise_for_status()
        return response.json()
        
    def create_group_chat_request(self, data):
        response = requests.post(
            f'{self.api_host}/chats',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': self.api_key,
                'x-client-id': 'websocket-server'   
            },
            json=data,
            verify=False
        )
        response.raise_for_status()
        return response.json()
    
    def get_group_chats(self):
        response = requests.get(
            f'{self.api_host}/chats',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': self.api_key,
                'x-client-id': 'websocket-server'   
            },
            verify=False
        )
        response.raise_for_status()
        return response.json()
         
    def join_group_chat_request(self, chat_id: str, session_id: str):
        response = requests.post(
            f'{self.api_host}/chats/{chat_id}/{session_id}',
            headers={
                'x-api-key': self.api_key,
                'x-client-id': 'websocket-server'   
            },
            verify=False
        )
        response.raise_for_status()
        return response.json()
        
    def left_group_chat_request(self, chat_id: str, session_id: str):
        response = requests.delete(
            f'{self.api_host}/chats/{chat_id}/{session_id}',
            headers={
                'x-api-key': self.api_key,
                'x-client-id': 'websocket-server'   
            },
            verify=False
        )
        response.raise_for_status()
        return response.json()
        
    def disconnect_user_request(self, data):
        response = requests.post(
            f'{self.api_host}/users/signoff',
            headers={
                'x-api-key': self.api_key,
                'x-client-id': 'websocket-server'   
            },
            json=data,
            verify=False
        )
        response.raise_for_status()
        return response.json()
        