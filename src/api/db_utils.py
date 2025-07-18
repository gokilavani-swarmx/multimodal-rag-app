import sqlite3, os
from datetime import datetime

# DB_NAME = "/src/sqlite_db/rag_app.db"
current_dir = os.getcwd()
os.makedirs(os.path.abspath(os.path.join(current_dir, "./src/sqlite_db/")), exist_ok=True)
DB_NAME = os.path.abspath(os.path.join(current_dir, "./src/sqlite_db/rag_app.db"))

def get_db_connection():
    # print(DB_NAME)
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_application_logs():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS application_logs
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     session_id TEXT,
                     user_query TEXT,
                     gpt_response TEXT,
                     model TEXT,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.close()

def insert_application_logs(session_id, user_query, gpt_response, model):
    conn = get_db_connection()
    conn.execute('INSERT INTO application_logs (session_id, user_query, gpt_response, model) VALUES (?, ?, ?, ?)',
                 (session_id, user_query, gpt_response, model))
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_query, gpt_response FROM application_logs WHERE session_id = ? ORDER BY created_at', (session_id,))
    messages = []
    for row in cursor.fetchall():
        messages.extend([
            {"role": "human", "content": row['user_query']},
            {"role": "ai", "content": row['gpt_response']}
        ])
    conn.close()
    return messages

def create_document_store():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS document_store
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              filename TEXT,
              filesize INTEGER,
              modified_date TIMESTAMP,
              upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              vec_db_creation_time_in_scnds REAL)''')
    conn.close()

def insert_document_record(filename, filesize=None, modified_date=None, vec_db_creation_time=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the file already exists in the database
    cursor.execute("SELECT id FROM document_store WHERE filename = ?", (filename,))
    existing_file = cursor.fetchone()

    if existing_file is None:
        # Insert the new file into the database
        cursor.execute("INSERT INTO document_store (filename, filesize, modified_date, vec_db_creation_time_in_scnds) VALUES (?, ?, ?, ?)",
                       (filename, filesize, modified_date, vec_db_creation_time  ))
        conn.commit()
        file_id = cursor.lastrowid  # Get the ID of the inserted row
        conn.close()
        return file_id
    else:
        file_id = existing_file[0]  # Get the ID of the existing file
        # print("file already exists in the database")
        conn.close()
        return (file_id, "file already exists in the database")
    
def insert_vec_db_creation_time(file_id, creation_time):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql_query = "UPDATE document_store SET vec_db_creation_time_in_scnds = ? WHERE id = ?"
    cursor.execute(sql_query, (creation_time, file_id)) 
    conn.close()

def delete_document_record(file_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM document_store WHERE id = ?', (file_id,))
    conn.commit()
    conn.close()
    return True

def get_all_documents():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, filename, upload_timestamp FROM document_store ORDER BY upload_timestamp DESC')
    documents = cursor.fetchall()
    conn.close()
    return [dict(doc) for doc in documents]

# Initialize the database tables
create_application_logs()
create_document_store()
