import requests
import urllib3

class RestService:

    host=''
    token=''
  
    def __init__(self, host, token):
        self.host = host
        self.token = token
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def store_group_message_request(self, 
        sender_id, 
        chat_id, 
        receivers, 
        message_content, 
        message_attachment
        ):
        
        try:
            response = requests.post(
                f'{self.host}/messages/group-messages',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.token}'
                },
                json={
                    'sender_id': sender_id,
                    'chat_id': chat_id,
                    'receivers': receivers,
                    'message': message_content,
                    'attachment': message_attachment
                },
                verify=False
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'store_group_message_request: {e}')
    
    def store_private_message_request(self, sender_id, receiver_id, message_content, message_attachment):
        try:
            response = requests.post(
                f'{self.host}/messages/private-messages',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.token}'
                },
                json={
                    'sender_id': sender_id,
                    'receiver_id': receiver_id,
                    'message': message_content,
                    'attachment': message_attachment
                },
                verify=False
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'store_private_message_request: {e}')

    def create_group_chat_request(self, session_id, chat_id, chat_name):
        try:
            response = requests.post(
                f'{self.host}/chats',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.token}'
                },
                json={
                    'chat_id': chat_id,
                    'chat_name': chat_name,
                    'session_id': session_id,
                },
                verify=False
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'create_group_chat_request: {e}')

    def get_group_chats(self):
        try:
            response = requests.get(
                f'{self.host}/chats',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.token}'
                },
                verify=False
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'get_group_chats: {e}')

    def join_group_chat_request(self, chat_id, session_id):
        try:
            response = requests.post(
                f'{self.host}/chats/{chat_id}/{session_id}',
                headers={
                    'Authorization': f'Bearer {self.token}'
                },
                verify=False
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'join_group_chat_request: {e}')

    def left_group_chat_request(self, chat_id, session_id):
        try:
            response = requests.delete(
                f'{self.host}/chats/{chat_id}/{session_id}',
                headers={
                    'Authorization': f'Bearer {self.token}'
                },
                verify=False
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'left_group_chat_request: {e}')
    
    def disconnect_user_request(self, user_id, session_id):
        try:
            response = requests.delete(
                f'{self.host}/users',
                headers={
                    'Authorization': f'Bearer {self.token}'
                },
                json={
                    'user_id': user_id,
                    'session_id': session_id
                },
                verify=False
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'disconnect_user_request: {e}')