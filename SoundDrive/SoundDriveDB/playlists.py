from .db import _connect

def _find_new_playlist_name() -> str:
    """
    Finds an unused playlist name
    :return: The new name
    """
    used_numbers = set()
    all_playlists = query()
    for playlist in all_playlists:
        if playlist[1].startswith("Playlist_"):
            try:
                number = int(playlist[1].split("_")[1])
                used_numbers.add(number)
            except ValueError:
                continue

    i = 1
    while i in used_numbers:
        i += 1
    return f"Playlist_{i}"

def create() -> None:
    """
    Create a playlist in the db
    :return: None
    """
    playlist_name = _find_new_playlist_name()

    conn, cursor = _connect()
    try:
        # Insert a new playlist
        cursor.execute('''
        INSERT INTO playlists (name)
        VALUES (?)
        ''', (playlist_name,))

        conn.commit()
    finally:
        conn.close()

def delete(playlist_id: int) -> None:
    """
    Delete a playlist from the db
    :param playlist_id: The id of the playlist to be deleted
    :return: None
    """
    print(f"Deleting playlist {playlist_id}")
    conn, cursor = _connect()
    try:
        cursor.execute('''
        DELETE FROM playlists
        WHERE id = ?
        ''', (playlist_id,))

        conn.commit()
    finally:
        conn.close()

def rename(playlist_id: int, new_name: str) -> None:
    """
    Rename a playlist
    :param playlist_id: The id of the playlist to be renamed
    :param new_name: The new name of the playlist
    :return: None
    """
    conn, cursor = _connect()
    try:
        # Update the songs list in the database
        cursor.execute('''
            UPDATE playlists
            SET name = ?
            WHERE id = ?
        ''', (new_name, playlist_id))

        conn.commit()
    finally:
        conn.close()

def add_song(playlist_id: int, song_id: int) -> None:
    """
    Add a song to a playlist
    :param playlist_id: The id of the playlist
    :param song_id: The id of the song
    :return: None
    """
    conn, cursor = _connect()
    try:
        # Fetch the current songs list
        cursor.execute('''
            SELECT songs FROM playlists
            WHERE id = ?
        ''', (playlist_id,))
        current_songs = cursor.fetchone()[0]

        # Append the new song_id to the list
        if current_songs:
            new_songs = current_songs + f',{song_id}'
        else:
            new_songs = str(song_id)

        # Update the songs list in the database
        cursor.execute('''
            UPDATE playlists
            SET songs = ?
            WHERE id = ?
        ''', (new_songs, playlist_id))
        conn.commit()
    finally:
        conn.close()

def query() -> list:
    """
    Query playlists from the db
    :return: The playlists
    """
    conn, cursor = _connect()

    try:
        cursor.execute('''
        SELECT * FROM playlists
        ''')
        playlists = cursor.fetchall()
        return playlists
    finally:
        conn.close()

def query_id(playlist_id: int) -> list:
    """
    Query playlist in db after id
    :param playlist_id: The id of the playlist
    :return: The playlist
    """
    conn, cursor = _connect()

    try:
        cursor.execute('''
        SELECT * FROM playlists
        WHERE id = ?
        ''', (playlist_id,))
        playlist = cursor.fetchall()
        return playlist[0]
    finally:
        conn.close()
