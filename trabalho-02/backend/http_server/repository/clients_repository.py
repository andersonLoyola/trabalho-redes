class ClientsRepository:
    
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool
        
    def get_client(self, api_key):
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            get_client_query = """
                SELECT 
                    id,
                    client_name,
                    status
                FROM clients c
                WHERE c.id = ?
            """
            cursor.execute(get_client_query, (api_key,))
            return cursor.fetchone()
        except Exception as e:
            print(f'create_private_message: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
       
 
  