# TODO: !IMPORTANT: GENERATE SSLA IF POSSIBLE, THIS WOULD MAKE US ENABLED TO USE HTTPS

import os

from http.server import HTTPServer
from infra.http import HTTPRequestHandler, HTTPRequestSerializer, HTTPRouter
from infra.database.conn import ConnectionPool

from repository import UsersRepository, ChatsRepository, MessagesRepository
from controllers import UsersController, ChatsController
from routes import TestRoutes, UserRoutes, ChatsRoutes
from services import TokenService, FileStorageService
from serializers import CryptoSerializer
from dotenv import load_dotenv

load_dotenv()


# -------- ENVIRONMENT VARIABLES -------------------
secret_key = os.getenv('secret_key')
chatuba_db_path=os.getenv('chatuba_db_path')
app_host = os.getenv('chatuba_app_host')
app_port = os.getenv('chatuba_app_port')
chatuba_webclient_host = os.getenv('chatuba_webclient_host')
# --------- SQLITE3 CONN POOL -----------
conn_pool = ConnectionPool(chatuba_db_path)
# --------- Repositories ----------------
chats_repository = ChatsRepository(conn_pool)
users_repository = UsersRepository(conn_pool)
messages_repository = MessagesRepository(conn_pool)
# --------- Serializers ----------------
crypto_serializer = CryptoSerializer(secret_key)
# --------- Services -------------------
token_service = TokenService(crypto_serializer)
file_storge_service = FileStorageService(app_host, app_port)
# --------- Controllers --------------
chats_controller = ChatsController(
    users_repository,
    chats_repository,
    messages_repository,
    crypto_serializer,
    token_service,
    file_storge_service,
)
users_controller = UsersController(
    users_repository, 
    crypto_serializer, 
    token_service
) 
# --------- infra ------------
http_request_parser = HTTPRequestSerializer()
http_router = HTTPRouter()
# ------- ROUTES ---------
# We dont really need this, the way it is working nowadays we are adding
# the routes directly to the router
userRoutes = UserRoutes(http_router, users_controller)
chatsRoutes = ChatsRoutes(http_router, chats_controller)
test_routes = TestRoutes(http_router)

HTTPRequestHandler.set_http_request_parser(http_request_parser)
HTTPRequestHandler.set_http_router(http_router)


if __name__ == '__main__':
    server = HTTPServer(( 'localhost', 8080), HTTPRequestHandler)
    print("HTTP Server Running...........")
    server.serve_forever()
