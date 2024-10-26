from .songs import query_all as songs_query_all
from .db import _connect
import threading

def create(artist_name: str) -> None:
    """
    Create artist in db
    :param artist_name: The name of the artist
    :return: None
    """
    if not isinstance(artist_name, str) or not artist_name:
        raise ValueError("Invalid song name")

    conn, cursor = _connect()
    try:
        # Insert a new song
        cursor.execute('''
        INSERT INTO artists (name)
        VALUES (?)
        ''', (artist_name,))

        conn.commit()
    finally:
        conn.close()

def query() -> list:
    """
    Query all artists
    :return: List of the artists
    """
    conn, cursor = _connect()

    try:
        cursor.execute('''
        SELECT * FROM artists
        ''')
        artists = cursor.fetchall()
        return artists
    finally:
        conn.close()

def query_name(artist_name: str) -> list:
    """
    Query an artist with a specific name from the db
    :param artist_name: The name of the artist
    :return: The artist
    """
    conn, cursor = _connect()

    try:
        cursor.execute('''
        SELECT * FROM artists
        WHERE name = ?
        ''', (artist_name,))
        artist = cursor.fetchall()
        if not artist:
            return []
        return artist[0]
    finally:
        conn.close()

def query_id(artist_id: int) -> list:
    """
    Query an artist with a specific id from the db
    :param artist_id: The id of the artist
    :return: The artist
    """
    conn, cursor = _connect()

    try:
        cursor.execute('''
        SELECT * FROM artists
        WHERE id = ?
        ''', (artist_id,))
        artist = cursor.fetchall()
        if not artist:
            return []
        return artist[0]
    finally:
        conn.close()

def check_db() -> None:
    """
    Check the integrity of the db
    :return: None
    """
    def check_all_artists_exist() -> None:
        """
        Checks if every artist can be found in the db
        If not, it adds them
        :return: None
        """
        all_songs = songs_query_all()
        for song in all_songs:
            for artist in song[3].split("/"):
                artist_data = query_name(artist)
                if not artist_data:
                    create(artist)

    check_paths_thread = threading.Thread(target=check_all_artists_exist)
    check_paths_thread.start()
