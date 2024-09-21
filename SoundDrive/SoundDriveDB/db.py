import sqlite3
import hashlib
import time

def _hash_file(file_path):
    start = time.time()
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    end = time.time()
    print(end - start)
    print(sha256_hash.hexdigest())
    return sha256_hash.hexdigest()

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
            hash TEXT,
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
