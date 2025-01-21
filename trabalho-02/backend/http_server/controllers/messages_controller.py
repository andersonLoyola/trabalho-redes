import traceback
from .base_controller import BaseController

class MessagesController(BaseController):

    def  __init__(
        self, 
        users_repository,
        chats_repository, 
        messages_repository,
        crypto_serializer,
        token_service,
        file_storage_service,
        clients_repository
    ):
        self.token_service = token_service
        self.chats_repository = chats_repository
        self.users_repository = users_repository
        self.messages_repository = messages_repository
        self.file_storage_service = file_storage_service
        super().__init__(crypto_serializer, clients_repository)

    def store_group_chat_messages(self, request):
        try:
            self.ensure_source(request['headers'].get('x-api-key'))
            attachment_data = ''
            request_body = self.decrypt_body(request['body'])
            found_chat = self.chats_repository.get_chat_by_id(request_body['chat_id'])
            if found_chat == None:
                return 404, {'message': 'chat not found'}
            if 'attachment' in request_body and request_body['attachment'] != '':
                attachment_data = {
                    **request_body['attachment']
                }
                attachment_data['file_path'] = self.file_storage_service.save_file(
                    request_body['sender_id'], 
                    request_body['attachment']
                )
                attachment_data = self.crypto_serializer.encrypt_values(attachment_data, ['file_size'])
            encrypted_message = self.crypto_serializer.encrypt_values(request_body, [
                'sender_id',
                'chat_id',
                'receivers',
                'init_vector',
                'attachment'
            ])
            self.messages_repository.create_group_message(
                encrypted_message['sender_id'],
                encrypted_message['chat_id'],
                encrypted_message['receivers'],
                encrypted_message['message'],
                encrypted_message['init_vector'],
                attachment_data
            )
            return 200, {   
                "message": "success",
            }
        except Exception as e:
            print(e)
            traceback.print_exc()  
            return 500, {"message": "internal server error"}
    
    def get_group_chat_messages(self, request):
        try:
            self.ensure_source(request['headers'].get('x-api-key'))
            request_body = self.decrypt_body(request['body'])
            user_sessions = self.users_repository.find_user_sessions(request_body['user_id'])
            found_chat = self.chats_repository.get_chat_by_name(request_body['chat_name'])
            if found_chat == None:
                return 404, {'message': 'chat not found'}
            found_group_messages = self.messages_repository.get_group_messages(
                user_sessions,
                found_chat['chat_id'],
            )
         
            return 200, self.encrypt_response({   
                "group_messages": found_group_messages
            })
        except Exception as e:
            print(e)
            traceback.print_exc()  
            return 500, {"message": "internal server error"}
   
    def store_private_chat_messages(self, request):
        try:
            self.ensure_source(request['headers'].get('x-api-key'))
            request_body = self.decrypt_body(request['body'])
            attachment_data = ''
            if 'attachment' in request_body and request_body['attachment'] != '':
                attachment_data = {
                    **request_body['attachment']
                }
                attachment_data['file_path'] = self.file_storage_service.save_file(
                    request_body['sender_id'], 
                    request_body['attachment']
                )
                attachment_data = self.crypto_serializer.encrypt_values(attachment_data, ['file_size'])
            encrypted_message = self.crypto_serializer.encrypt_values(request_body, [
                'sender_id',
                'receiver_id',
                'attachment',
                'init_vector'
            ])
            self.messages_repository.create_private_message(
                encrypted_message['sender_id'],
                encrypted_message['receiver_id'],
                encrypted_message['message'],
                encrypted_message['init_vector'],
                attachment_data
            )
            return 200, {   
                "message": "success",
            }
        except Exception as e:
            print(e)
            traceback.print_exc()  
            return 500, {"message": "internal server error"}
    
