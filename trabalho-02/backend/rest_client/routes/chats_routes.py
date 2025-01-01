class ChatsRoutes():
    def __init__(self, http_router, chats_controller):
        self.http_router = http_router
        self.chats_controller = chats_controller
        self.add_routes()

    def add_routes(self):
        # self.http_router.add_url_rule('/api/chats/<chat_id>', 'get_chat_details', self.chats_controller.get_chat_details, methods=['GET'])
        # self.http_router.add_url_rule('/api/chats/<chat_id>/<user_id>', 'join_chat', self.chats_controller.join_chat, methods=['POST'])
        # self.http_router.add_url_rule('/api/chats/<chat_id>', 'add_chat_users', self.add_chat_users, methods=['POST'])
        # self.http_router.add_url_rule('/api/chats/<chat_id>', 'get_chat_details', self.get_chat_details, methods=['GET'])
        self.http_router.add_url_rule('chats', '/api/v1/chats', 'create_chat', self.create_chat, 'POST')
        # self.http_router.add_url_rule('/api/chats', 'get_user_chats', self.get_user_chats, methods=['GET'])
    

    def create_chat(self, request):
        return self.chats_controller.create_chat(request)
    
    def add_chat_users(self, request):
        return self.chats_controller.add_chat_users(request)
    
    def get_user_chats(self, request):
        return self.chats_controller.get_user_chats(request)
    
    def get_chat_details(self, request):
        return self.chats_controller.get_chat_details(request)
    
    