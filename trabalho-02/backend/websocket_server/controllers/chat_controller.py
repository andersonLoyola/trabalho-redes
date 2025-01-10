import traceback

class ChatController():

    def __init__(
            self,
            actions_queue,  
            connections_service,      
            messages_service
        ):
        self.actions_queue = actions_queue
        self.messages_service = messages_service
        self.connections_service = connections_service
        # ---- DISABLE THIS TO PREVENT USING DB DATA ---- #
        self.connections_service.load_group_chats()

    def handle_available_chats_request(self, client_socket):
        response = self.connections_service.get_available_chats()
        self.messages_service.send_message(client_socket, response)
    
    def handle_available_users_request(self, client_socket):
        response = self.connections_service.get_available_users()
        self.messages_service.send_message(client_socket, response)

    def handle_send_group_message_request(self, decoded_data, client_socket):
        chat_id = decoded_data['chat_id']

        found_chat = self.connections_service.get_chat_connection(chat_id)
        
        if found_chat == None:
            self.messages_service.send_message(
                client_socket, 
                {'error': 'chat not found', 'action': 'group_message'}
            )
            return 
        
        store_message_action = {
            **decoded_data,
            'receivers': []
        }
        
        for subscriber_id in found_chat['subscribers']:
            response = self.connections_service.get_user_connection(subscriber_id, chat_id)
            if 'error' not in response:
                self.messages_service.send_message(response['conn'], decoded_data)
                store_message_action['receivers'].append(response['user_id'])
            else:
                print(response['error'])
        self.actions_queue.add_action(store_message_action)
       
    def handle_send_private_message_request(self, decoded_data, client_socket):
        decoded_data['action'] = 'private_message'
        
        if decoded_data['attachment']:
            attachment_data = decoded_data['attachment']
            file_path = self.file_storage_service.save_file(attachment_data)
            decoded_data['attachment'] = file_path
        
        found_user = self.connections_service.get_user_connection(decoded_data['receiver_id'])
        if found_user == None: 
            self.messages_service.send_message(client_socket, {
                'error': 'user not found', 
                'action': 'private_message'
            })

        if 'socket' in found_user:
            self.messages_service.send_message(found_user['socket'], decoded_data)
            self.messages_service.send_message(client_socket, decoded_data)
        self.messages_service.store_private_messages(
            decoded_data['sender_id'], 
            decoded_data['receiver_id'], 
            decoded_data['message'], 
            decoded_data['attachment']
        )

    def handle_create_group_connection(self, decoded_data, client_socket):
        response = self.connections_service.create_group_connection(decoded_data)
        self.messages_service.send_message(client_socket, response)

    # --- Bothe private and group chats will be treated as chat
    def handle_join_chat_request(self, decoded_data, client_socket):
        chat_id = decoded_data['chat_id']
        user_id = decoded_data['user_id']

        response = self.connections_service.add_user_chat_session(user_id, chat_id, client_socket)
        self.messages_service.send_message(client_socket, response)
        self.actions_queue.add_action(decoded_data)
    
    def handle_left_chat_request(self, decoded_data, client_socket):
        response = self.connections_service.join_left_connection(decoded_data)
        self.messages_service.send_message(client_socket, response)

    def handle_connection_request(self, decoded_data, client_socket):
        response = self.connections_service.connect_user(decoded_data)
        self.messages_service.send_message(client_socket, response)

    def handle_disconnect_request(self, decoded_data, client_socket):
        if decoded_data == None:
            return
        
        if 'user_id' in decoded_data:
            self.connections_service.remove_user_active_session(decoded_data['user_id'], client_socket)
        elif 'sender_id' in decoded_data:
            self.connections_service.remove_user_active_session(decoded_data['sender_id'], client_socket)

        # client_socket.close()

    def handle_ping(self, client_socket):
        self.messages_service.send_message(client_socket, 'PONG')

    def handle_client(self, client_socket):
        try:
            self.messages_service.receive_handshake_message(client_socket)
            while True:
                decoded_data = self.messages_service.receive_message(client_socket)
                if not decoded_data:
                    pass
                elif decoded_data == 'PING':
                    self.handle_ping(client_socket)
                elif decoded_data['action'] == 'connection':
                    self.handle_connection_request(decoded_data, client_socket)
                elif decoded_data['action'] == 'available_chats':
                    self.handle_available_chats_request(client_socket)
                elif decoded_data['action'] == 'available_users':
                    self.handle_available_users_request(client_socket)
                elif decoded_data['action'] == 'group_message':
                    self.handle_send_group_message_request(decoded_data, client_socket)
                elif decoded_data['action'] == 'private_message':
                    self.handle_send_private_message_request(decoded_data, client_socket)
                elif decoded_data['action'] == 'join_chat':
                    self.handle_join_chat_request(decoded_data, client_socket)
                elif decoded_data['action'] == 'left_connection':
                    self.handle_left_chat_request(decoded_data, client_socket)
                elif decoded_data['action'] == 'disconnect':
                    self.handle_disconnect_request(client_socket)
                    return
    
                
        except (ConnectionResetError, ConnectionAbortedError) as e:
            traceback.print_exc()
            self.handle_disconnect_request(decoded_data, client_socket)
            print(e)
            return 

        except Exception as e:
            traceback.print_exc()   
            # decoded_data['error'] = e
            # self.messages_service.send_message(client_socket, decoded_data)
            print(e)
            return

        
           
        