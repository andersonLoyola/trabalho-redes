
class MessagesRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_messages_by_ids(self, message_ids): 
        masks = ['?' for _ in message_ids]
        query = f"""
          SELECT * FROM messages
          WHERE id IN {masks}
        """
        cursor = self.conn.cursor()
        results = cursor.execute(query, list(message_ids))
        return results.fetchall()
