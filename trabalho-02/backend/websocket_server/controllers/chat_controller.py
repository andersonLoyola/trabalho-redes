import traceback
class ChatController():

    def __init__(self, messages_service, file_storage_service, connections_service, auth_service):
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
        response = self.auth_service.handle_auth_request(decoded_data)
        user_data = response['user']
        if 'error' in response:
            self.messages_service.send_message(client_socket, response)

        response = self.connections_service.has_connections_available()
        if 'error' in response:
            self.messages_service.send_message(client_socket, response)
        
        response = self.connections_service.add_connection(user_data, client_socket)
        response['user'] = user_data
        self.messages_service.send_message(client_socket, response)

    def handle_available_connections(self, decoded_data, client_socket):
        response = self.connections_service.get_available_chats()
        self.messages_service.send_message(client_socket, response)
    
    def handle_available_users(self, decoded_data, client_socket):
        response = self.connections_service.get_available_users()
        self.messages_service.send_message(client_socket, response)

    def handle_send_message(self, decoded_data, client_socket):
        del decoded_data['request_type']
        decoded_data['response_type'] = 'message'
        
        if decoded_data['attachment']:
            file = decoded_data['attachment']
            file_path = self.file_storage_service.save_file(file)
            decoded_data['attachment'] = file_path
        if 'chat_id' in decoded_data:
            #TODO: add verification for group chat later
            found_chat = self.connections_service.get_chat_connection(decoded_data['chat_id'])
            for subscriber_id in found_chat['subscribers']:
                receiver = self.connections_service.get_user_connection(subscriber_id)
                if receiver != None and 'socket' in receiver:
                    self.messages_service.send_message(receiver['socket'], decoded_data)
        elif 'user_id' in decoded_data:
            found_user = self.connections_service.get_user_connection(decoded_data['user_id'])
            self.messages_service.send_message(found_user['socket'], decoded_data)
        self.messages_service.send_message(client_socket, decoded_data)

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

    def handle_client(self,  client_socket = {}):
        try:
            self.messages_service.receive_handshake_message(client_socket)
            while True:
                decoded_data = self.messages_service.receive_message(client_socket)
                if not decoded_data:
                    return
                if decoded_data['request_type'] == 'signup':
                    self.handle_signup_request(decoded_data, client_socket)
                if decoded_data['request_type'] == 'auth':
                   self.handle_auth_request(decoded_data, client_socket)
                elif decoded_data['request_type'] == 'create_group_connection':
                    self.handle_create_group_connection(decoded_data, client_socket)
                elif decoded_data['request_type'] == 'available_chats':
                    self.handle_available_connections(decoded_data,client_socket)
                elif decoded_data['request_type'] == 'available_users':
                    self.handle_available_users(decoded_data,client_socket)
                elif decoded_data['request_type'] == 'message':
                    self.handle_send_message(decoded_data, client_socket)
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
            self.messages_service.send_message(client_socket, decoded_data)
            print(e)
            return

        
           
        