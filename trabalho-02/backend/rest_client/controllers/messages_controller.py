import traceback

class MessagesController:

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

    def store_group_chat_messages(self, request):
        try:
            token = request['headers'].get('Authorization').split(' ')[-1]
            request_body = request['body']
            decoded_token = self.token_service.decode_token(token)
            if (not decoded_token or 'id' not in decoded_token ):
                return 401, {'message': 'unauthorized'}
            found_chat = self.chats_repository.get_chat_by_id(request_body['chat_id'])
            if found_chat == None:
                return 404, {'message': 'chat not found'}
            if 'attachment' in request_body and request_body['attachment'] != '':
                request_body['attachment']['file_path'] = self.file_storage_service.save_file(request_body['sender_id'], request_body['attachment'])
            self.messages_repository.create_group_message(
                request_body['sender_id'],
                request_body['chat_id'],
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
   
    def store_private_chat_messages(self, request):
        try:
            token = request['headers'].get('Authorization').split(' ')[-1]
            request_body = request['body']
            decoded_token = self.token_service.decode_token(token)
            if (not decoded_token or 'id' not in decoded_token ):
                return 401, {'message': 'unauthorized'}
            # found_user = self.users_repository.get_user_by_session_id(request_body['session_id'])
            # if found_user == None:
            #     return 404, {'message': 'chat not found'}
            if 'attachment' in request_body and request_body['attachment'] != '':
                request_body['attachment']['file_path'] = self.file_storage_service.save_file(request_body['sender_id'], request_body['attachment'])
            self.messages_repository.create_private_message(
                request_body['sender_id'],
                request_body['receiver_id'],
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
    
