class AuthService:
    def __init__(self, user_repository):
        self.users_repository = user_repository

    def handle_auth_request(self, decoded_data):
        username = decoded_data['username']
        password = decoded_data['password']

        found_user = self.users_repository.get_user(username)

        if not found_user:
            return {'error': 'user not found', 'response_type': 'auth'}
            
        if found_user['password'] != password:
            return {'error': 'invalid password', 'response_type': 'auth'}

        return {
            'success': True, 
            'response_type': 'auth', 
            'user': {
                'user_id': found_user['id'],
                'username': found_user['username'],
            }
        }
    
    def handle_signup_request(self, decoded_data):
        username = decoded_data['username']
        password = decoded_data['password']

        found_user = self.users_repository.get_user(username)

        if found_user:
            return{'error': 'user already exists', 'response_type': 'signup'}
        
        self.users_repository.create_user(username, password)
        return {'success': True, 'response_type': 'signup'}

    