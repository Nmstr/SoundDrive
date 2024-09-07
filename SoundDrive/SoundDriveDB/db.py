import sqlite3

def _connect():
    """
    Connects to the database
    """
    conn = sqlite3.connect('SoundDrive.db')
    cursor = conn.cursor()
    return conn, cursor

def create_db() -> None:
    conn, cursor = _connect()

    try:
        # Create the songs table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            filepath TEXT NOT NULL,
            artist TEXT,
            deleted BOOLEAN DEFAULT 0
        )
        ''')

        # Create the playlists table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            cover TEXT,
            songs TEXT
        )
        ''')

        conn.commit()
    finally:
        conn.close()