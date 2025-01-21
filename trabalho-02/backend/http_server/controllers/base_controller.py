import json

class BaseController:

    def __init__(self, crypto_serializer, clients_repository):
        self.crypto_serializer = crypto_serializer
        self.clients_repository = clients_repository

    def ensure_source(self, api_key):
        found_client_info = self.clients_repository.get_client(api_key)
        if not found_client_info:
            raise Exception('Client not foud')
        if found_client_info['status'] != 'ENABLED':
            raise Exception(f'Client {found_client_info['client_name']} not allowed to peform action')
    
    def _decrypt_request_body(self, request_body):
        decrypted_data = self.crypto_serializer.decrypt(request_body)
        return decrypted_data
    
    def _encrypt_response_body(self, response_body):
        return self.crypto_serializer.encrypt(json.dumps(response_body).encode('utf-8'))

    def _encrypt_web_socket_response_body(self, response_body, keys_to_ignore):
        encrypted_response = self.crypto_serializer.encrypt_values(response_body, keys_to_ignore)
        return encrypted_response
   
    def decrypt_body(self, request_body):
        return self._decrypt_request_body(request_body)
         
    def encrypt_response(self, response_body):
        return self._encrypt_response_body(response_body)