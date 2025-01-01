import traceback


class ChatController():

    def __init__(self, chats_repository, messages_service, jwt_service, file_storage_service):
        self.connections = {}
        self.jwt_service = jwt_service
        self.chats_repository = chats_repository
        self.messages_service = messages_service
        self.file_storage_service = file_storage_service
        self.MAX_CONNECTIONS = 5
    

    def handle_file_upload_request(self, file_data):
        file_name = file_data['file_name']
        # file_size = file_data['file_size'] define later
        file_data = file_data['file_data']
        self.file_storage_service.save_file(file_data, file_name)

    def handle_group_message_request(self, client_socket, decoded_data):
        try:
            chat = self.chats_repository.get_chat_participants(decoded_data['chat_id'])
            if decoded_data['attachment'] != '':
                self.handle_file_upload_request(decoded_data['attachment'])
                decoded_data['attachment'] = self.file_storage_service.generate_attachment_link(decoded_data['attachment'])
            chat_id = decoded_data['chat_id']
            for participant_id in chat['users']:
                if participant_id in self.connections and participant_id != decoded_data['sender_id']:
                    receiver_id = f'{participant_id}_{chat_id}'
                    receiver_socket = self.connections[chat_id][receiver_id]
                    self.messages_service.send_messaage(receiver_socket, decoded_data)
            self.messages_service.send_message(client_socket, decoded_data)
            self.messages_service.store_messages(
                decoded_data['sender_id'], 
                decoded_data['chat_id'], 
                decoded_data['content'], 
                decoded_data['attachment']
            )
        except Exception as e:
            traceback.print_stack()
            print(e)
            return

    def handle_private_message_request(self, client_socket, decoded_data):
        receiver_id = decoded_data['receiver_id']
        sender_id = decoded_data['sender_id']
        self.messages_service.send_message(client_socket, decoded_data)
        if receiver_id in self.connections:
            receiver_socket = self.connections[receiver_id][f'{receiver_id}_{sender_id}']
            self.messages_service.send_message(receiver_socket, decoded_data) 
        self.messages_service.store_messages(
            decoded_data['sender_id'], 
            decoded_data['receiver_id'], 
            decoded_data['content'], 
            decoded_data['attachment']
        )

    def handle_auth_request(self, decoded_data, client_socket):
    
        token = decoded_data['auth_token']
        decoded_token = self.jwt_service.decode_token(token)
            
        if not decoded_token:
            self.messages_service.send_message(client_socket, {'error': 'Invalid token'})
            self.handle_disconnect_request(client_socket)
            return
        if len(self.connections) > self.MAX_CONNECTIONS:
            self.messages_service.send_message(client_socket, {'error': 'max connections reached'})
            self.handle_disconnect_request(client_socket)
            return   
             
        self.connections[decoded_token['user_id']] = {
            'username': decoded_token['username'],
            'connection': client_socket
        }
        
    def handle_disconnect_request(self, client_socket):
        self.messages_service.send_message(client_socket, {'message': 'disconnected'})
        for user_id in self.connections:
            if self.connections[user_id]['socket'] == client_socket:
                del self.connections[user_id]
                break
        client_socket.close()

    def handle_client(self,  client_socket = {}):
        try:

            self.messages_service.receive_handshake_message(client_socket)

            while True:
                decoded_data = self.messages_service.receive_message(client_socket)
                if not decoded_data:
                    continue
                if decoded_data['request_type'] == 'auth':
                   self.handle_auth_request(decoded_data, client_socket)
                elif decoded_data['request_type'] == 'duo_message':
                    self.handle_private_message_request(client_socket,decoded_data)
                elif decoded_data['request_type'] == 'disconnect':
                    if decoded_data['user_id'] in self.connections:
                        self.handle_disconnect_request(client_socket)
                elif decoded_data['request_type'] == 'group_message':
                    self.handle_group_message_request(client_socket, decoded_data)
        except (ConnectionResetError, ConnectionAbortedError) as e:
            traceback.print_stack()
            self.handle_disconnect_request(client_socket)
            print(e)
            return 

        except Exception as e:
            traceback.print_stack()   
            print(e)
            return

        
           
        