import requests

class RestService:
    
    host=''
    token=''
    instance = None

    def __init__(self, host, token):
        self.host = host
        self.token = token

    @classmethod
    def get_instance(cls, host, token):
        if not cls.instance:
            cls.instance = RestService(host, token)
        return cls.instance

    def store_group_message_request(self, message):
        try:
            chat_id = message['chat_id']
            response = requests.post(
                f'{self.host}/chats/{chat_id}/messages',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.token}'
                },
                json=message
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)
    
    def store_private_message_request(self, message):
        try:
            response = requests.post(
                self.host,
                headers={
                    'Content-Type': 'application/json',
                },
                json=message
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)

    def join_group_chat_request(self, chat_id, user_id):
        try:
            response = requests.post(
                self.host,
                headers={
                    'Content-Type': 'application/json',
                },
                json={
                    'chat_id': chat_id,
                    'user_id': user_id
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)

    def get_group_chats(self):
        try:
            response = requests.get(
                f'{self.host}/chats',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.token}'
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)