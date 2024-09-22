from .db import _connect
import threading
import os

def create(song_name: str, file_path: str, artist_names: str = "") -> None:
    """
    Create song in db
    """
    if not isinstance(song_name, str) or not song_name:
        raise ValueError("Invalid song name")
    if not isinstance(file_path, str) or not file_path:
        raise ValueError("Invalid file path")
    if artist_names is None:
        artist_names = []
    if not isinstance(artist_names, str):
        raise ValueError("Invalid artist names")

    conn, cursor = _connect()
    try:
        # Insert a new song
        cursor.execute('''
        INSERT INTO songs (name, filepath, artist)
        VALUES (?, ?, ?)
        ''', (song_name, file_path, artist_names))

        conn.commit()
    finally:
        conn.close()

def mark_as_deleted(song_id: int, value: int) -> None:
    """
    Mark song as deleted
    """
    conn, cursor = _connect()

    try:
        cursor.execute('''
        UPDATE songs
        SET deleted = ?
        WHERE id = ?
        ''', (value, song_id,))

        conn.commit()
    finally:
        conn.close()

def query() -> list:
    """
    Query songs in db
    """
    conn, cursor = _connect()

    try:
        cursor.execute('''
        SELECT * FROM songs
        WHERE deleted = 0
        ''')
        songs = cursor.fetchall()
        return songs
    finally:
        conn.close()

def query_all() -> list:
    """
    Query all songs in db (including deleted)
    """
    conn, cursor = _connect()

    try:
        cursor.execute('''
        SELECT * FROM songs
        ''')
        songs = cursor.fetchall()
        return songs
    finally:
        conn.close()

def query_id(song_id: int) -> list:
    """
    Query songs in db after id
    """
    conn, cursor = _connect()

    try:
        cursor.execute('''
        SELECT * FROM songs
        WHERE id = ?
        ''', (song_id,))
        song = cursor.fetchall()
        if not song:
            return []
        return song[0]
    finally:
        conn.close()

def query_path(song_path: str) -> list:
    """
    Query songs in db after path
    """
    conn, cursor = _connect()

    try:
        cursor.execute('''
        SELECT * FROM songs
        WHERE filepath = ?
        ''', (song_path,))
        song = cursor.fetchall()
        if not song:
            return []
        return song[0]
    finally:
        conn.close()

def check_db():
    def check_song_paths():
        all_songs = query_all()
        for song in all_songs:
            if not os.path.isfile(song[2]):
                mark_as_deleted(song[0], 1)
            elif song[4] == 1:
                mark_as_deleted(song[0], 0)

    check_paths_thread = threading.Thread(target=check_song_paths)
    check_paths_thread.start()
