import requests

class ChatsService():

    def __init__(self, url):
        self.url = url

    
    def load_chats_info(self, token):
        try:
            response = requests.get(
                f'{self.url}/chats',
                headers={'Authorization': f'Bearer {token}'}
            )
            return response.json()
        except Exception as e:
            print(e)
            return {'error': str(e)}
    
    def load_chat_details(self, token, chat_id):
        try:
            response = requests.get(
                f'{self.url}/chats/{chat_id}',
                headers={'Authorization': f'Bearer {token}'}
            )
            return response.json()
        except Exception as e:
            print(e)
            return {'error': str(e)}
    
    def create_chat(self, token, name, chat_type):
        try:
            response = requests.post(
                f'{self.url}/chats',
                headers={'Authorization': f'Bearer {token}'},
                json={'name': name, 'chat_type': chat_type}
            )
            return response.json()
        except Exception as e:
            print(e)
            return {'error': str(e)}
