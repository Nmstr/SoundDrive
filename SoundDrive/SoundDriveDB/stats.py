from .artists import query_name as artists_query_name
from .songs import query_id as songs_query_id
from .db import _connect

class Stats:
    def __init__(self) -> None:
        pass

    def add_to_history(self, song_id: int) -> None:
        """
        Add a song to the history
        :param song_id: The id of the song
        :return: None
        """
        song_data = songs_query_id(song_id)
        artists = song_data[3].split("/")
        artist_ids = []
        for artist in artists:
            artist_data = artists_query_name(artist)
            artist_ids.append(str(artist_data[0]))

        conn, cursor = _connect()
        try:
            # Insert a new song
            cursor.execute('''
            INSERT INTO stats_history (song_id, artist_id, duration_played)
            VALUES (?, ?, ?)
            ''', (song_id, ",".join(artist_ids), 0))

            conn.commit()
        finally:
            conn.close()
