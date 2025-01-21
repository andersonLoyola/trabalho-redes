import ssl

from infra.http import HTTPRequestHandler, HTTPRequestSerializer, HTTPRouter, ThreadedHTTPServer
from infra.database.conn import ConnectionPool

from repository import UsersRepository, ChatsRepository, MessagesRepository, ClientsRepository
from controllers import UsersController, ChatsController, MessagesController
from routes import TestRoutes, UserRoutes, ChatsRoutes, MessagesRoutes
from services import TokenService, FileStorageService
from serializers import CryptoSerializer
import config

# --------- SQLITE3 CONN POOL -----------
conn_pool = ConnectionPool(config.database_path)
# --------- Repositories ----------------
chats_repository = ChatsRepository(conn_pool)
users_repository = UsersRepository(conn_pool)
messages_repository = MessagesRepository(conn_pool)
clients_repository = ClientsRepository(conn_pool)
# --------- Serializers ----------------
crypto_serializer = CryptoSerializer(config.crypto_secret_key)
# --------- Services -------------------
token_service = TokenService(crypto_serializer)
file_storge_service = FileStorageService(config.http_server_host, config.http_server_port)
# --------- Controllers --------------
messages_controller = MessagesController(
    users_repository,
    chats_repository,
    messages_repository,
    crypto_serializer,
    token_service,
    file_storge_service,
    clients_repository
)
chats_controller = ChatsController(
    users_repository,
    chats_repository,
    messages_repository,
    crypto_serializer,
    token_service,
    clients_repository
)
users_controller = UsersController(
    users_repository, 
    crypto_serializer, 
    token_service,
    clients_repository
) 
# --------- infra ------------
http_request_parser = HTTPRequestSerializer()
http_router = HTTPRouter()
# ------- ROUTES ---------
userRoutes = UserRoutes(http_router, users_controller)
chatsRoutes = ChatsRoutes(http_router, chats_controller)
messagesRoutes = MessagesRoutes(http_router, messages_controller)
test_routes = TestRoutes(http_router)

HTTPRequestHandler.set_http_request_parser(http_request_parser)
HTTPRequestHandler.set_http_router(http_router)

# https://stackoverflow.com/questions/4818280/ssl-wrap-socket-attributeerror-module-object-has-no-attribute-wrap-socket
# https://stackoverflow.com/questions/22429648/ssl-in-python3-with-httpserver
if __name__ == '__main__':
    try:
        httpd = ThreadedHTTPServer((config.http_server_host, config.http_server_port), HTTPRequestHandler)
        sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        sslctx.check_hostname = False # If set to True, only the hostname that matches the certificate will be accepted
        sslctx.load_cert_chain(certfile='certificate.pem', keyfile="key.pem")
        httpd.socket = sslctx.wrap_socket(httpd.socket, server_side=True)
        print("HTTPS Server Running...........")
        httpd.serve_forever()
    except Exception as e:
        print(str(e))
    finally:
        httpd.server_close()