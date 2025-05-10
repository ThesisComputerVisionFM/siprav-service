import sqlite3


def get_db():
    conn = sqlite3.connect("cameras.db")
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cameras (
            camera_id TEXT PRIMARY KEY,
            location TEXT,
            status TEXT,
            timestamp TEXT,
            person_count INTEGER
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")