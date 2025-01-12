class MessagesRoutes():
    def __init__(self, http_router, chats_controller):
        self.http_router = http_router
        self.chats_controller = chats_controller
        self.add_routes()

    def add_routes(self):
        self.http_router.add_url_rule('messages','/api/v1/messages/group-messages', 'store_chat_messages', self.store_group_chat_messages, 'POST')
        self.http_router.add_url_rule('messages','/api/v1/messages/private-messages', 'store_private_chat_messages', self.store_private_chat_messages, 'POST')
    
    def store_group_chat_messages(self, request):
        return self.chats_controller.store_group_chat_messages(request)
   
    def store_private_chat_messages(self, request):
        return self.chats_controller.store_private_chat_messages(request)
    
