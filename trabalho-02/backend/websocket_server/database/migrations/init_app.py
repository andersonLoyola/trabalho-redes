"""
    https://stackoverflow.com/questions/15856976/transactions-with-python-sqlite3
"""

import sqlite3

connection = sqlite3.connect('../chatuba_db.sqlite3')
connection.isolation_level = None

cursor = connection.cursor()

create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id VARCHAR(36) PRIMARY KEY NOT NULL UNIQUE,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL 
    );
"""

create_chats_table = """
    CREATE TABLE IF NOT EXISTS chats (
        id VARCHAR(36) PRIMARY KEY NOT NULL UNIQUE,
        name VARCHAR(255) NOT NULL UNIQUE,
        users TEXT
    );
"""

create_messages_table = """
    CREATE TABLE IF NOT EXISTS messages (
        id VARCHAR(36) PRIMARY KEY NOT NULL UNIQUE,
        sender_id VARCHAR(36) NOT NULL,
        chat_id VARCHAR(36) NOT NULL,
        content TEXT,
        attachment TEXT
    );
"""

create_attachments_table = """
    CREATE TABLE IF NOT EXISTS attachments (
        id VARCHAR(36) PRIMARY KEY NOT NULL UNIQUE,
        file_name VARCHAR(255) NOT NULL,
        file_path TEXT NOT NULL
    );
"""

cursor.execute("BEGIN")

try:
    cursor.execute(create_users_table)
    cursor.execute(create_chats_table)
    cursor.execute(create_messages_table)
    cursor.execute(create_attachments_table)
    cursor.execute("COMMIT")
except Exception as e:
    cursor.execute("ROLLBACK")
    print(e)