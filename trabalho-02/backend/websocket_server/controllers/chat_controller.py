import traceback

class ChatController():

    def __init__(self, auth_service, connections_service, file_storage_service, messages_service):
        self.auth_service = auth_service
        self.messages_service = messages_service
        self.connections_service = connections_service
        self.file_storage_service = file_storage_service
        # ---- DISABLE THIS TO PREVENT USING DB DATA ---- #
        self.connections_service.preload_chat_conns()

    def handle_signup_request(self, decoded_data, client_socket):
        response = self.auth_service.handle_signup_request(decoded_data)
        self.messages_service.send_message(client_socket, response)
    
    def handle_auth_request(self, decoded_data, client_socket):
        auth_response = self.auth_service.handle_auth_request(decoded_data)
        if 'error' in auth_response:
            self.messages_service.send_message(client_socket, auth_response)
            return
        # TODO: pretty sure this shouldnt be here, we need to put this in the app.py so we cnan prevent the user
        #  from connecting
        conn_available_response = self.connections_service.has_connections_available()
        if 'error' in conn_available_response:
            self.messages_service.send_message(client_socket, conn_available_response)
            return
        
        self.connections_service.add_connection(auth_response['user'], client_socket)
        self.messages_service.send_message(client_socket, auth_response)

    def handle_available_connections(self, client_socket):
        response = self.connections_service.get_available_chats()
        self.messages_service.send_message(client_socket, response)
    
    def handle_available_users(self, client_socket):
        response = self.connections_service.get_available_users()
        self.messages_service.send_message(client_socket, response)

    def handle_send_group_message(self, decoded_data, client_socket):
        del decoded_data['request_type']
        decoded_data['response_type'] = 'group_message'
        if decoded_data['attachment']:
            attachment_data = decoded_data['attachment']
            file_path = self.file_storage_service.save_file(attachment_data)
            decoded_data['attachment'] = file_path
        #TODO: add verification for group chat later
        found_chat = self.connections_service.get_chat_connection(decoded_data['chat_id'])
        if found_chat == None:
            self.messages_service.send_message(
                client_socket, 
                {'error': 'chat not found', 'response_type': 'group_message'}
            )
        for subscriber_id in found_chat['subscribers']:
            found_user = self.connections_service.get_user_connection(subscriber_id, decoded_data['chat_id'])
            if 'socket' in found_user:
                self.messages_service.send_message(found_user['socket'], decoded_data)
        self.messages_service.store_group_messages(
            decoded_data['sender_id'], 
            decoded_data['chat_id'],
            found_chat['subscribers'], 
            decoded_data['message'], 
            decoded_data['attachment']
        )
       
    def handle_send_private_message(self, decoded_data, client_socket):
        del decoded_data['request_type']
        decoded_data['response_type'] = 'private_message'
        
        if decoded_data['attachment']:
            attachment_data = decoded_data['attachment']
            file_path = self.file_storage_service.save_file(attachment_data)
            decoded_data['attachment'] = file_path
        
        found_user = self.connections_service.get_user_connection(decoded_data['receiver_id'])
        if found_user == None: 
            self.messages_service.send_message(client_socket, {
                'error': 'user not found', 
                'response_type': 'private_message'
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

    def handle_join_group_connection(self, decoded_data, client_socket):
        response = self.connections_service.join_group_connection(decoded_data)
        self.messages_service.send_message(client_socket, response)
    
    def handle_left_group_connection(self, decoded_data, client_socket):
        response = self.connections_service.join_left_connection(decoded_data)
        self.messages_service.send_message(client_socket, response)

    def handle_disconnect_request(self, client_socket):
        self.connections_service.remove_user_connection(client_socket)
        client_socket.close()

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
                elif decoded_data['request_type'] == 'signup':
                    self.handle_signup_request(decoded_data, client_socket)
                elif decoded_data['request_type'] == 'auth':
                   self.handle_auth_request(decoded_data, client_socket)
                elif decoded_data['request_type'] == 'create_group_connection':
                    self.handle_create_group_connection(decoded_data, client_socket)
                elif decoded_data['request_type'] == 'available_chats':
                    self.handle_available_connections(client_socket)
                elif decoded_data['request_type'] == 'available_users':
                    self.handle_available_users(client_socket)
                elif decoded_data['request_type'] == 'group_message':
                    self.handle_send_group_message(decoded_data, client_socket)
                elif decoded_data['request_type'] == 'private_message':
                    self.handle_send_private_message(decoded_data, client_socket)
                elif decoded_data['request_type'] == 'join_group_connection':
                    self.handle_join_group_connection(decoded_data, client_socket)
                elif decoded_data['request_type'] == 'left_group_connection':
                    self.handle_left_group_connection(decoded_data, client_socket)
                elif decoded_data['request_type'] == 'disconnect':
                    self.handle_disconnect_request(client_socket)
                    return
    
                
        except (ConnectionResetError, ConnectionAbortedError) as e:
            traceback.print_stack()
            self.handle_disconnect_request(client_socket)
            print(e)
            return 

        except Exception as e:
            traceback.print_stack()   
            # decoded_data['error'] = e
            # self.messages_service.send_message(client_socket, decoded_data)
            print(e)
            return

        
           
        