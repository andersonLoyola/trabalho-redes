from http.server import HTTPServer
from infra import HTTPRequestHandler, HTTPRequestSerializer, HTTPRouter
import jwt
import os
import sqlite3

from repository import UsersRepository, ChatsRepository
from controllers import UsersController,ChatsController
from serializers import ChatSerializer, MessagesSerializer, SqliteSerializer
# from routes import UserRoutes, ChatsRoutes
from services import JwtService
# from routes import ChatsRoutes
from routes import TestRoutes, UserRoutes, ChatsRoutes
from dotenv import load_dotenv

load_dotenv()



jwt_secret = os.getenv('jwt_secret')

chatuba_db_path=os.getenv('chatuba_db_path')

app_host = os.getenv('chatuba_app_host')
app_port = os.getenv('chatuba_app_port')

chatuba_webclient_host = os.getenv('chatuba_webclient_host')




jwtService = JwtService(jwt, jwt_secret)

conn = sqlite3.connect(chatuba_db_path)



conn.row_factory = SqliteSerializer.to_dict

# messagesRepository = MessagesRepository(db)
# messagesSerializer = MessagesSerializer()


chatsRepository = ChatsRepository(conn)
# chatsSerializer = ChatSerializer()
chatsController = ChatsController(
    jwtService, 
    chatsRepository, 
    {}, 
    {}, 
    {},
    {},
)
http_request_parser = HTTPRequestSerializer()
http_router = HTTPRouter()

userRepository = UsersRepository(conn)
usersController = UsersController(userRepository, jwtService)
userRoutes = UserRoutes(http_router, usersController)

chatsRoutes = ChatsRoutes(http_router, chatsController)


test_routes = TestRoutes(http_router)


HTTPRequestHandler.set_http_request_parser(http_request_parser)
HTTPRequestHandler.set_http_router(http_router)



if __name__ == '__main__':
    server = HTTPServer(( 'localhost', 8080), HTTPRequestHandler)
    print("HTTP Server Running...........")
    server.serve_forever()
