"""
    https://stackoverflow.com/questions/15856976/transactions-with-python-sqlite3
"""
import uuid
import sqlite3

def execute(): 
    connection = sqlite3.connect('../db.sqlite3')
    connection.isolation_level = None

    cursor = connection.cursor()

    create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) PRIMARY KEY NOT NULL UNIQUE,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            init_vector_id VARCHAR(36) NOT NULL UNIQUE,
            FOREIGN KEY(init_vector_id) REFERENCES init_vectors(id) 
        );
    """

    create_user_sessions_table = """
        CREATE TABLE IF NOT EXISTS user_sessions (
            user_id VARCHAR(36) NOT NULL,
            session_id VARCHAR(36) NOT NULL,
            status VARCHAR(36) NOT NULL DEFAULT 'ACTIVE',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """

    create_chats_table = """
        CREATE TABLE IF NOT EXISTS chats (
            id VARCHAR(36) PRIMARY KEY NOT NULL UNIQUE,
            name VARCHAR(255) NOT NULL UNIQUE
        );
    """

    create_private_messages_table = """
        CREATE TABLE IF NOT EXISTS private_messages (
            sender_id VARCHAR(36) NOT NULL,
            receiver_id VARCHAR(36) NOT NULL,
            content TEXT,
            attachment_id VARCHAR(36) DEFAULT '',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            init_vector_id VARCHAR(36) NOT NULL,
            FOREIGN KEY(sender_id) REFERENCES user_sessions(session_id),
            FOREIGN KEY(receiver_id) REFERENCES user_sessions(session_id),
            FOREIGN KEY(attachment_id) REFERENCES attachments(id)
            FOREIGN KEY(init_vector_id) REFERENCES init_vectors(id)
        );
    """

    create_group_messages_table = """
        CREATE TABLE IF NOT EXISTS group_messages (
            sender_id VARCHAR(36) NOT NULL,
            chat_id VARCHAR(36) NOT NULL,
            receiver_id VARCHAR(36) NOT NULL,
            content TEXT,
            attachment_id VARCHAR(36) DEFAULT '',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            init_vector_id VARCHAR(36) NOT NULL, 
            FOREIGN KEY(chat_id) REFERENCES chats(id)
            FOREIGN KEY(attachment_id) REFERENCES attachments(id)
            FOREIGN KEY(init_vector_id) REFERENCES init_vectors(id)
            FOREIGN KEY(sender_id) REFERENCES user_sessions(session_id)
            FOREIGN KEY(receiver_id) REFERENCES user_sessions(session_id)
        );
    """

    create_attachments_table = """
        CREATE TABLE IF NOT EXISTS attachments (
            id VARCHAR(36) PRIMARY KEY NOT NULL UNIQUE,
            file_format VARCHAR(255) NOT NULL,
            file_size VARCHAR(255) NOT NULL,
            file_name VARCHAR(255) NOT NULL,
            init_vector_id VARCHAR(36) NOT NULL,
            file_path TEXT NOT NULL,
            FOREIGN KEY(init_vector_id) REFERENCES init_vectors(id)
        );
    """

    user_chats_query = """
        CREATE TABLE IF NOT EXISTS chat_users (
            user_session_id VARCHAR(36) NOT NULL,
            chat_id VARCHAR(36) NOT NULL,
            FOREIGN KEY(chat_id) REFERENCES chats(id),
            FOREIGN KEY(user_session_id) REFERENCES user_sessions(session_id),
            UNIQUE(user_session_id, chat_id)
        )
    """
   
    group_messages_indexes = """
        CREATE INDEX idx_sender_receiver
        ON group_messages(receiver_id, sender_id)
    """

    user_sessions_session_id_index = """
        CREATE INDEX idx_session_id
        ON user_sessions(session_id)
    """

    user_sessions_user_id_index = """
        CREATE INDEX idx_user_id
        ON user_sessions(user_id)
    """

    create_init_vector_query = """
        CREATE TABLE IF NOT EXISTS init_vectors (
            id VARCHAR(36) PRIMARY KEY NOT NULL,
            init_vector TEXT NOT NULL 
        )
    """

    create_clients_table = """
        CREATE TABLE IF NOT EXISTS clients (
            id varchar(36) PRIMARY KEY NOT NULL,
            client_name VARCHAR(50) NOT NULL UNIQUE,
            status VARCHAR(50) NOT NULL DEFAULT 'ENABLED'
        );
    """
    
    create_clients_table_idx = """
        CREATE INDEX idx_client_name 
        ON clients(client_name)
    """

    def init_clients(clients: list[str], cursor: sqlite3.Cursor) -> str: 
        for client in clients:
            client_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO clients(
                    id,
                    client_name
                ) VALUES (
                    ?,
                    ?
                )
            """, (client_id, client))
            print(f'{client}: {client_id}')
            


    try:
        cursor.execute("BEGIN;")
        cursor.execute(create_users_table)
        cursor.execute(create_chats_table)
        cursor.execute(create_attachments_table)
        cursor.execute(create_private_messages_table)
        cursor.execute(create_group_messages_table)
        cursor.execute(create_user_sessions_table)
        cursor.execute(user_chats_query)
        cursor.execute(group_messages_indexes)
        cursor.execute(user_sessions_session_id_index)
        cursor.execute(user_sessions_user_id_index)
        cursor.execute(create_init_vector_query)
        cursor.execute(create_clients_table)
        cursor.execute(create_clients_table_idx)
        init_clients(['cmd-client', 'websocket-server', 'test-testudo'], cursor)
        connection.commit()
    except Exception as e:
        cursor.execute("ROLLBACK;")
        connection.rollback()
        print(str(e))
        raise e
    
execute()