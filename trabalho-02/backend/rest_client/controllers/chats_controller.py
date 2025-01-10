import traceback

class ChatsController:

    def  __init__(
            self, 
            users_repository,
            chats_repository, 
            messages_repository,
            crypto_serializer,
            token_service,
            file_storage_service,

        ):
        self.token_service = token_service
        self.chats_repository = chats_repository
        self.users_repository = users_repository
        self.crypto_serializer = crypto_serializer
        self.messages_repository = messages_repository
        self.file_storage_service = file_storage_service

    def create_chat(self, request):
        try:
            request_data = request['body']
            token = request['headers'].get('Authorization').split(' ')[-1]
            decoded_token = self.token_service.decode_token(token)
            if (not decoded_token or 'id' not in decoded_token ):
                return 401, {'message': 'unauthorized'}
            found_chat = self.chats_repository.get_chat_by_name(request_data['chat_name'])
            if (found_chat):
                return 409, {'message': 'chat with the same name found'}
            created_chat_id = self.chats_repository.create_chat(
                chat_name = request_data['chat_name'],
                user_id = decoded_token['id'],
            )
            return 200, { "message": "success", 'created_chat_id': created_chat_id }
    
        except Exception as e:
            print(e)
            traceback.print_exc()  
            return 500, {"message": "internal server error"}
    
    def get_available_chats(self, request):
        try:
            token = request['headers'].get('Authorization').split(' ')[1]
            decoded_token = self.token_service.decode_token(token)
            if (not decoded_token or 'id' not in decoded_token ):
                return 401, {'message': 'unauthorized'}
            chats = self.chats_repository.get_chats_info()
            return 200, { "message": "success", "chats": chats}
        except Exception as e:
            print(e)
            traceback.print_exc()
            return 500, { "message": "internal server error"}
        
    def get_chat_details(self, request, chat_id):
        try:
            token = request['headers'].get('Authorization').split(' ')[1]
            decoded_token = self.token_service.decode_token(token)
            if (not decoded_token or 'id' not in decoded_token ):
                return 401, {'message': 'unauthorized'}
            chat = self.chats_repository.get_chat_details(chat_id)
            return 200, { 
                "message": "success",
                "chat": chat,
            }
        except Exception as e:
            print(e)
            traceback.print_exc()  
            return 500, {"message": "internal server error"}
   
    def add_chat_participant(self, request, chat_id):
        try:
            token = request['headers'].get('Authorization').split(' ')[1]
            decoded_token = self.token_service.decode_token(token)
            if (not decoded_token or 'id' not in decoded_token ):
                return 401, {'message': 'unauthorized'}
            chat = self.chats_repository.add_chat_participant(chat_id, decoded_token['id'])
            return 200, { 
                "message": "success",
            }
        except Exception as e:
            print(e)
            traceback.print_exc()  
            return 500, {"message": "internal server error"}

    def store_group_chat_messages(self, request, chat_id):
        try:
            token = request['headers'].get('Authorization').split(' ')[1]
            request_body = request['body']
            decoded_token = self.token_service.decode_token(token)
            
            if (not decoded_token or 'id' not in decoded_token ):
                return 401, {'message': 'unauthorized'}
            found_chat = self.chats_repository.get_chat_by_id(chat_id)
            if found_chat == None:
                return 404, {'message': 'chat not found'}
            if 'attachment' in request_body and request_body['attachment'] != '':
                request_body['attachment']['file_path'] = self.file_storage_service.save_file(request_body['sender_id'], request_body['attachment'])
            self.messages_repository.create_group_message(
                request_body['sender_id'],
                chat_id,
                request_body['receivers'],
                request_body['message'],
                request_body['attachment']
            )
            return 200, { 
                "message": "success",
            }
        except Exception as e:
            print(e)
            traceback.print_exc()  
            return 500, {"message": "internal server error"}

   