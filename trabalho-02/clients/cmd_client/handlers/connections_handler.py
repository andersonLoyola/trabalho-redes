import time

class ConnectionsHandler:
    
    message_service = {}
    MAX_RETRY_ATTEMPT = 3

    def __init__(self, message_service):
        self.message_service = message_service

    def _apply_exponential_backoff(self, retry_attempt):
        backoff_time = 5 * (2 ** (retry_attempt - 1))
        time.sleep(backoff_time)

    def _send_user_connection_message(self, conn, user_data_info):
        connection_message = {
            'user_id': user_data_info['id'],
            'user_name': user_data_info['username'],
            'session_id': user_data_info['session_id'],
            'action': 'connection'
        }
        self.message_service.send_message(conn, connection_message)
        response = self.message_service.receive_message(conn)
        return response
    
    def connection_handler(self, conn, user_data_info):
        retry_attempt = 0
        while True:
            response = self._send_user_connection_message(conn, user_data_info)
            if 'success' in response:
                return response
            elif 'error' in response:
                if retry_attempt < 3:
                    input(f'error: {response['error']}')
                    retry_attempt += 1
                    self._apply_exponential_backoff(retry_attempt)
                else:
                    input(f'error: {response['error']}')
                    return