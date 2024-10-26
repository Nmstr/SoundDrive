import sqlite3

def _connect() -> tuple:
    """
    Connects to the database
    Returns: The connection and cursor in a tuple
    """
    conn = sqlite3.connect('SoundDrive.db')
    cursor = conn.cursor()
    return conn, cursor

def create_db() -> None:
    """
    Creates the database and its tables
    :return: None
    """
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

        # Create artists table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        ''')

        # Create history table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            song_id INTEGER,
            artist_id INTEGER,
            played_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            duration_played INTEGER
        )
        ''')

        conn.commit()
    finally:
        conn.close()
