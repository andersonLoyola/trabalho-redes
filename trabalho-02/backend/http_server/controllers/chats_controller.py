import traceback

from .base_controller import BaseController
class ChatsController(BaseController):

    def  __init__(
        self, 
        users_repository,
        chats_repository, 
        messages_repository,
        crypto_serializer,
        token_service,
        clients_repository
    ):
        self.token_service = token_service
        self.chats_repository = chats_repository
        self.users_repository = users_repository
        self.messages_repository = messages_repository
        super().__init__(crypto_serializer, clients_repository)

    def create_chat(self, request):
        try:
            self.ensure_source(request['headers'].get('x-api-key'))
            chat_data = self.decrypt_body(request['body'])
            found_chat = self.chats_repository.get_chat_by_name(chat_data['chat_name'])
            if (found_chat):
                return 409, {'message': 'chat with the same name found'}
            created_chat_id = self.chats_repository.create_chat(
                chat_id = chat_data['chat_id'],
                chat_name = chat_data['chat_name'],
                session_id = chat_data['session_id']
            )
            return 200, { "message": "success", 'created_chat_id': created_chat_id } 
        except Exception as e:
            print(e)
            traceback.print_exc()  
            return 500, {"message": "internal server error"}
    
    def get_available_chats(self, request):
        try:
            self.ensure_source(request['headers'].get('x-api-key'))
            chats = self.chats_repository.get_chats_info()
            return 200, { "message": "success", "chats": chats}
        except Exception as e:
            print(e)
            traceback.print_exc()
            return 500, { "message": "internal server error"}
        
    def get_chat_details(self, request, chat_id):
        try:
            self.ensure_source(request['headers'].get('x-api-key'))
            chat = self.chats_repository.get_chat_details(chat_id)
            return 200, { 
                "message": "success",
                "chat": chat,
            }
        except Exception as e:
            print(e)
            traceback.print_exc()  
            return 500, {"message": "internal server error"}
   
    def add_chat_participant(self, request, chat_id, session_id):
        try:
            self.ensure_source(request['headers'].get('x-api-key'))
            found_participation = self.chats_repository.get_chat_participant(chat_id, session_id)
            if found_participation == None:
                self.chats_repository.add_chat_participant(chat_id, session_id)
            return 200, { 
                "message": "success",
            }
        except Exception as e:
            print(e)
            traceback.print_exc()  
            return 500, {"message": "internal server error"}

    def remove_chat_participant(self, request, chat_id, session_id):
        try:
            self.ensure_source(request['headers'].get('x-api-key'))
            found_chat = self.chats_repository.get_chat_by_id(chat_id)
            if found_chat == None:
                return 404, {'message': 'chat not found'}
            self.chats_repository.remove_chat_participant(
              chat_id,
              session_id 
            )
            return 200, {   
                "message": "success",
            }
        except Exception as e:
            print(e)
            traceback.print_exc()  
            return 500, {"message": "internal server error"}

    def get_user_chats(self, request, user_id):
        self.ensure_source(request['headers'].get('x-api-key'))
        user_chats = self.users_repository.find_user_sessions(user_id)
        return 200, self.encrypt_response({'chats': user_chats})