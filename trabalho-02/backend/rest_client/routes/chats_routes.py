from flask import request

class ChatsRoutes():
    def __init__(self, app, chats_controller):
        self.app = app
        self.chats_controller = chats_controller
        self.add_routes()

    def add_routes(self):
        # self.app.add_url_rule('/api/chats/<chat_id>', 'get_chat_details', self.chats_controller.get_chat_details, methods=['GET'])
        # self.app.add_url_rule('/api/chats/<chat_id>/<user_id>', 'join_chat', self.chats_controller.join_chat, methods=['POST'])
        self.app.add_url_rule('/api/chats/<chat_id>', 'add_chat_users', self.add_chat_users, methods=['POST'])
        self.app.add_url_rule('/api/chats/<chat_id>', 'get_chat_details', self.get_chat_details, methods=['GET'])
        self.app.add_url_rule('/api/chats', 'create_chat', self.create_chat, methods=['POST'])
        self.app.add_url_rule('/api/chats', 'get_user_chats', self.get_user_chats, methods=['GET'])
    

    def create_chat(self):
        return self.chats_controller.create_chat(request)
    
    def add_chat_users(self, chat_id):
        return self.chats_controller.add_chat_users(request, chat_id)
    
    def get_user_chats(self):
        return self.chats_controller.get_user_chats(request)
    
    def get_chat_details(self, chat_id):
        return self.chats_controller.get_chat_details(request, chat_id)
    
    