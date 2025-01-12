class ChatsRoutes():
    def __init__(self, http_router, chats_controller):
        self.http_router = http_router
        self.chats_controller = chats_controller
        self.add_routes()

    def add_routes(self):
        self.http_router.add_url_rule('chats','/api/v1/chats/<chat_id>/<session_id>', 'add_chat_participant', self.add_chat_participant, 'POST')
        self.http_router.add_url_rule('chats','/api/v1/chats/<chat_id>/<session_id>', 'remove_chat_participant', self.remove_chat_participant, 'DELETE')
        self.http_router.add_url_rule('chats','/api/v1/chats/<chat_id>', 'get_chat_details', self.get_chat_details, 'GET')
        self.http_router.add_url_rule('chats', '/api/v1/chats', 'get_available_chats', self.get_available_chats, 'GET')
        self.http_router.add_url_rule('chats', '/api/v1/chats', 'create_chat', self.create_chat, 'POST')
    
    def create_chat(self, request):
        return self.chats_controller.create_chat(request)
    
    def add_chat_participant(self, request, chat_id, session_id):
        return self.chats_controller.add_chat_participant(request, chat_id, session_id)
    
    def get_available_chats(self, request):
        return self.chats_controller.get_available_chats(request)
    
    def get_chat_details(self, request, chat_id):
        return self.chats_controller.get_chat_details(request, chat_id)
  
    def remove_chat_participant(self, request, chat_id, session_id):
        return self.chats_controller.remove_chat_participant(request, chat_id, session_id)