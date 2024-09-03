from .db import _connect

def _find_new_playlist_name() -> str:
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

def query(playlist_name: str = None) -> list:
    """
    Query playlists from the db

    Returns all playlists, if no name is given. Otherwise, returns the named playlist.
    """
    conn, cursor = _connect()

    if playlist_name:
        try:
            cursor.execute('''
            SELECT * FROM playlists
            WHERE name = ?
            ''', (playlist_name,))
            playlists = cursor.fetchall()
            return playlists
        finally:
            conn.close()
    else:
        try:
            cursor.execute('''
            SELECT * FROM playlists
            ''')
            playlists = cursor.fetchall()
            return playlists
        finally:
            conn.close()
