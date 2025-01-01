from jwt  import InvalidTokenError, ExpiredSignatureError
import traceback

class ChatsController():

    def  __init__(
            self, 
            jwtService, 
            chatsRepository, 
            messagesRepository, 
            usersRepository,
            chatsSerializer,
            messagesSerializer
        ):
        self.jwtService = jwtService
        self.chatsRepository = chatsRepository
        self.usersRepository = usersRepository
        self.messagesRepository = messagesRepository
        self.chatsSerializer = chatsSerializer

    def create_chat(self, request):
        try:
            token = request['headers'].get('Authorization').split(' ')[1]
            request_data = request['body']
            decoded_token = self.jwtService.decode_token(token)
            created_chat_id = self.chatsRepository.create_chat(
                chat_type = request_data['chat_type'], 
                chat_name = request_data['chat_name'],
                user_id = decoded_token['user_id']
            )
        
            return 200, { "message": "success", 'created_chat_id': created_chat_id }
        except ExpiredSignatureError as e:
            print(e)
            traceback.print_exc()  
            return 401, {"message": "token has expired"} 
        except InvalidTokenError as e:
            print(e)
            traceback.print_exc()  
            return 401, {"message": "invalid token"}
        except Exception as e:
            print(e)
            traceback.print_exc()  
            return 500, {"message": "internal server error"}

    # def add_chat_users(self, request, chat_id):
    #     try: 
    #         token = request.headers.get('Authorization').split(' ')[1]
    #         decoded_token = self.jwtService.decode_token(token)
    #         request_data = request.get_json()
    #         # A user can only add users to a chat if he is already member of the chat
    #         chat = self.chatsRepository.get_chat_details(chat_id)
    #         if decoded_token['user_id'] not in chat['users']:
    #             return { "message": "unauthorized"}), 401
    #         #TODO: ADDS THIS LATER We can only add users that are already registered
    #         self.chatsRepository.add_users(chat_id, request_data['users'])
    #         return { "message": "success"}), 200
    #     except ExpiredSignatureError as e:
    #         print(e)
    #         traceback.print_exc()  
    #         return jsonify({"message": "token has expired"}), 401
    #     except InvalidTokenError as e:
    #         print(e)
    #         traceback.print_exc()  
    #         return jsonify({"message": "invalid token"}), 401
    #     except Exception as e:
    #         print(e)
    #         traceback.print_exc()  
    #         return jsonify({"message": "internal server error"}), 500

    # def get_user_chats(self, request):
    #     bearer_token = request.headers.get('Authorization').split(' ')[1]
    #     try:
    #         decoded_token = self.jwtService.decode_token(bearer_token)
    #     except Exception as e:
    #         return jsonify({ "message": "invalid token"}), 401
    #     chats = self.chatsRepository.get_user_chats(decoded_token['user_id'])
    #     mapped_chats = self.chatsSerializer.map_chats_info(chats)
    #     return jsonify({ "message": "success", "chats": mapped_chats}), 200
        
    # def get_chat_details(self, request, chat_id):
    #     try:
    #         token = request.headers.get('Authorization').split(' ')[1]
    #         self.jwtService.decode_token(token)
    #         chat = self.chatsRepository.get_chat_details(chat_id)
    #         chat_users = self.usersRepository.get_users_by_ids(chat['users'])
    #         chat_messages = self.messagesRepository.get_messages_by_ids(chat['messages'])
    #         mapped_messages = self.messagesSerializer.serialize_messages(chat_messages)
    #         mapped_chat = self.chatsSerializer.map_chat_details(chat, mapped_messages, chat_users)
    #         return jsonify({ 
    #             "message": "success",
    #             "chat": mapped_chat,
    #         }), 200

    #     except ExpiredSignatureError as e:
    #         print(e)
    #         traceback.print_exc()  
    #         return jsonify({"message": "token has expired"}), 401
    #     except InvalidTokenError as e:
    #         print(e)
    #         traceback.print_exc()  
    #         return jsonify({"message": "invalid token"}), 401
    #     except Exception as e:
    #         print(e)
    #         traceback.print_exc()  
    #         return jsonify({"message": "internal server error"}), 500

   