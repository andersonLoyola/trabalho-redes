import traceback
import threading
class ChatController:

    def __init__(
            self,
            actions_queue,  
            connections_service,      
            messages_service,
            group_chats_service
        ):
        self.actions_queue = actions_queue
        self.messages_service = messages_service
        self.connections_service = connections_service
        self.group_chats_service = group_chats_service
        self._lock = threading.Lock()

    def handle_create_group_chat_request(self, client_socket, decoded_data):
        response = self.group_chats_service.create_group_chat(
            decoded_data['user_id'], 
            decoded_data['session_id'],
            decoded_data['chat_name']
        )
        self.messages_service.send_message(client_socket, response)

    def handle_show_group_chats_request(self, client_socket):
        response = self.group_chats_service.show_group_chats()
        self.messages_service.send_message(client_socket, response)
    
    def handle_show_private_chats_request(self, client_socket):
        response = self.connections_service.show_private_chats()
        self.messages_service.send_message(client_socket, response)

    def handle_send_group_message_request(self, decoded_data, client_socket):
        with self._lock:
            chat_id = decoded_data['chat_id']
            found_chat = self.group_chats_service.get_chat_connection(chat_id)
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
            for subscriber_data in found_chat['subscribers']:
                response = self.connections_service.get_user_session(
                    subscriber_data['user_id'], 
                    subscriber_data['session_id'],
                    chat_id,
                )
                if not response:
                    pass
                elif 'error' not in response:
                    self.messages_service.send_message(response['conn'], decoded_data)
                    store_message_action['receivers'].append(response['user_id'])
                else:
                    print(response['error'])
            self.actions_queue.add_action(store_message_action)
       
    def handle_send_private_message_request(self, decoded_data, client_socket): 
        found_user = self.connections_service.get_user_session(
            decoded_data['receiver_id'], 
            decoded_data['receiver_session'], 
            decoded_data['sender_id']
        )
        if found_user == None: 
            self.messages_service.send_message(client_socket, {
                'error': 'user not found', 
                'action': 'private_message'
            })
            return
        if 'conn' in found_user:
            self.messages_service.send_message(found_user['conn'], decoded_data)
            self.messages_service.send_message(client_socket, decoded_data)
        self.actions_queue.add_action({
            'sender_id':decoded_data['sender_id'], 
            'receiver_id': decoded_data['receiver_id'], 
            'message':decoded_data['message'], 
            'attachment': decoded_data['attachment'],
            'action': 'private_message'
        })

    def handle_create_group_chat(self, decoded_data, client_socket):
        response = self.group_chats_service.create_group_chat(
            decoded_data['user_id'],
            decoded_data['session_id'],
            decoded_data['chat_name']    
        )
        self.messages_service.send_message(client_socket, response)

    def handle_join_group_chat_request(self, decoded_data, client_socket):
        user_id = decoded_data['user_id']
        chat_id = decoded_data['chat_id']
        session_id = decoded_data['session_id']
        group_chat = self.group_chats_service.get_chat_connection(chat_id)
        if group_chat != None:
            self.connections_service.update_session_status(user_id, session_id, 'busy', chat_id)
            response = self.group_chats_service.add_user_chat_session(user_id, session_id, chat_id)
            self.messages_service.send_message(client_socket, response)
        
    # Review this later TODO:
    def handle_join_private_chat_request(self, decoded_data, client_socket):
        user_id = decoded_data['user_id']
        session_id = decoded_data['session_id']
        receiver_id = decoded_data['receiver_id']
        receiver_session = decoded_data['receiver_session']

        found_user = self.connections_service.get_user_session(receiver_id, receiver_session, session_id)

        if found_user != None:
            self.connections_service.update_session_status(user_id, session_id, 'busy', receiver_session)
            self.messages_service.send_message(client_socket, {'success': True})
        
    # maybe we dont really need this 
    def handle_left_private_chat(self, decoded_data, client_socket):
        self.connections_service.update_session_status(decoded_data['user_id'], decoded_data['session_id'], 'active', '')
        self.messages_service.send_message(client_socket, {'success': True})

    def handle_left_chat_request(self, decoded_data, client_socket):
        response = self.group_chats_service.left_group_connection(decoded_data)
        self.connections_service.update_session_status(decoded_data['user_id'], decoded_data['session_id'], 'active', '')
        self.messages_service.send_message(client_socket, response)

    def handle_connection_request(self, decoded_data, client_socket):
        response = self.connections_service.connect_user(decoded_data, client_socket)
        self.messages_service.send_message(client_socket, response)

    def handle_disconnect_request(self, decoded_data, client_socket):
        if decoded_data == None:
            return
        if 'user_id' in decoded_data:
            self.connections_service.remove_user_active_session(decoded_data['user_id'], client_socket)
        elif 'sender_id' in decoded_data:
            self.connections_service.remove_user_active_session(decoded_data['sender_id'], client_socket)

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
                elif decoded_data['action'] == 'show_group_chats':
                    self.handle_show_group_chats_request(client_socket)
                elif decoded_data['action'] == 'group_message':
                    self.handle_send_group_message_request(decoded_data, client_socket)
                elif decoded_data['action'] == 'create_group_chat':
                    self.handle_create_group_chat(decoded_data, client_socket)
                elif decoded_data['action'] == 'left_group_chat':
                    self.handle_left_chat_request(decoded_data, client_socket)
                elif decoded_data['action'] == 'left_private_cha':
                    self.handle_left_private_chat(decoded_data, client_socket)
                elif decoded_data['action'] == 'show_private_chats':
                    self.handle_show_private_chats_request(client_socket)
                elif decoded_data['action'] == 'private_message':
                    self.handle_send_private_message_request(decoded_data, client_socket)
                elif decoded_data['action'] == 'join_group_chat':
                    self.handle_join_group_chat_request(decoded_data, client_socket)
                elif decoded_data['action'] == 'join_private_chat':
                    self.handle_join_private_chat_request(decoded_data, client_socket)
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
            self.handle_disconnect_request(decoded_data, client_socket)
            print(e)
            return

        
           
        