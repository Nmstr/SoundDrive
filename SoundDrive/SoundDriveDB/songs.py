from .db import _connect

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
        INSERT INTO songs (name, filepath, artist, hash)
        VALUES (?, ?, ?, ?)
        ''', (song_name, file_path, artist_names, 'hash_value'))

        conn.commit()
    finally:
        conn.close()

def mark_as_deleted() -> None:
    """
    Mark song as deleted
    """
    conn, cursor = _connect()

    try:
        cursor.execute('''
        UPDATE songs
        SET deleted = 1
        WHERE id = ?
        ''', (1,))

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

def query_id(song_id: int) -> list:
    """
    Query songs in db after id
    """
    conn, cursor = _connect()

    try:
        cursor.execute('''
        SELECT * FROM songs
        WHERE deleted = 0
        AND id = ?
        ''', (song_id,))
        song = cursor.fetchall()
        return song[0]
    finally:
        conn.close()
