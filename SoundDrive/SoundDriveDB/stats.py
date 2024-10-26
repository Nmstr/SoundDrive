from .artists import query_name as artists_query_name
from .songs import query_id as songs_query_id
from .db import _connect

class Stats:
    def __init__(self) -> None:
        pass

    def get_history(self) -> list:
        conn, cursor = _connect()

        try:
            cursor.execute('''
            SELECT * FROM stats_history
            ''')
            history = cursor.fetchall()
            return history
        finally:
            conn.close()

    def get_history_for_id(self, song_id: int) -> list:
        conn, cursor = _connect()

        try:
            cursor.execute('''
            SELECT * FROM stats_history WHERE song_id=?
            ''', (song_id,))
            history = cursor.fetchall()
            return history
        finally:
            conn.close()

    def add_to_history(self, song_id: int, played_time: float) -> None:
        """
        Add a song to the history
        :param song_id: The id of the song
        :param played_time: The time the song was played for
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
            ''', (song_id, ",".join(artist_ids), played_time))

            conn.commit()
        finally:
            conn.close()
