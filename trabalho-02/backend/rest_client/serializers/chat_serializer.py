class ChatSerializer():

    def map_user_chats(self, chat):
        mapped_chat = {}
        mapped_chat['_id'] = str(chat['_id'])
        mapped_chat['chat_name'] = chat['chat_name']
        mapped_chat['chat_type'] = chat['chat_type']
        return mapped_chat
    
    def map_chat_info(self, chat):
        mapped_chat = {}
        mapped_chat['_id'] = str(chat['_id'])
        mapped_chat['users'] = chat['users']
        mapped_chat['chat_name'] = chat['chat_name']
        mapped_chat['messages'] = chat['messages']
        mapped_chat['chat_type'] = chat['chat_type']
        return mapped_chat

    def map_chat_details(self, chat, chat_messages, chat_users):

        users_details = {
            str(user['_id']): {
                '_id': str(user['_id']),
                'username': user['username']
            }
            for user in chat_users
        }
        
        messages_details = [{
            '_id': str(message['_id']), 
            'content': message['content'], 
            'timestamp': message['timestamp'], 
            'sender': users_details[message['sender_id']]['username'],
            'receiver': users_details[message['receiver_id']]['username'],
        } for message in chat_messages]

        return {
            '_id': chat['_id'],
            'chat_name': chat['chat_name'],
            'chat_type': chat['chat_type'],
            'users': list(users_details.values()),
            'messages': messages_details
        }
    
    def map_chats_info(self, chats):
        return [self.map_chat_info(chat) for chat in chats]
    
    def map_chats_details(self, chats, chat_messages, chat_users):
        return [self.map_chat_details(chat, chat_messages, chat_users) for chat in chats]