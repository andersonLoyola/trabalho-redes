from http.server import HTTPServer
from infra import HTTPRequestHandler, HTTPRequestSerializer, HTTPRouter

import os
# from repository import ChatsRepository, UsersRepository, MessagesRepository
# from controllers import UsersController, ChatsController
# from serializers import ChatSerializer, MessagesSerializer
# from routes import UserRoutes, ChatsRoutes
# from services import JwtService
# from routes import ChatsRoutes
from routes import TestRoutes
from dotenv import load_dotenv

load_dotenv()



jwt_secret = os.getenv('jwt_secret')
mongo_uri = os.getenv('mongo_uri')
app_host = os.getenv('chatuba_app_host')
app_port = os.getenv('chatuba_app_port')

chatuba_webclient_host = os.getenv('chatuba_webclient_host')




# jwtService = JwtService(jwt, jwt_secret)

# messagesRepository = MessagesRepository(db)
# messagesSerializer = MessagesSerializer()

# userRepository = UsersRepository(db)
# usersController = UsersController(userRepository, jwtService)
# userRoutes = UserRoutes(app, usersController)

# chatsRepository = ChatsRepository(db)
# chatsSerializer = ChatSerializer()
# chatsController = ChatsController(
#     jwtService, 
#     chatsRepository, 
#     messagesRepository, 
#     userRepository, 
#     chatsSerializer,
#     messagesSerializer,
# )
# chatsRoutes = ChatsRoutes(app, chatsController)
http_request_parser = HTTPRequestSerializer()
http_router = HTTPRouter()

test_routes = TestRoutes(http_router)


HTTPRequestHandler.set_http_request_parser(http_request_parser)
HTTPRequestHandler.set_http_router(http_router)



if __name__ == '__main__':
    server = HTTPServer(( 'localhost', 8080), HTTPRequestHandler)
    print("HTTP Server Running...........")
    server.serve_forever()
