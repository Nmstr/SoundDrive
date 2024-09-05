from mutagen import File
import PySoundSphere

class MusicController:
    def __init__(self, db_access) -> None:
        self.player = PySoundSphere.AudioPlayer("pygame")
        self.player.volume = 0.075
        self.db_access = db_access
        self._timeline = []
        self._timeline_position = 0
        self._current_playlist = None
        self._playlist_position = 0

    def _reload_playback(self) -> None:
        self.player.load(self._timeline[self._timeline_position - 1])
        self.player.stop()
        self.player.play()

    def play(self, song_path: str) -> None:
        self._timeline = self._timeline[:self._timeline_position]
        self._timeline_position += 1
        self._timeline.append(song_path)
        self._reload_playback()

    def continue_playback(self) -> None:
        self.player.play()

    def stop(self) -> None:
        self.player.pause()

    def next(self) -> None:
        print(self._timeline, self._timeline_position, self._current_playlist, self._playlist_position)
        if self._timeline_position < len(self._timeline):
            self._timeline_position += 1
            self._reload_playback()
        elif self._current_playlist is not None and self._playlist_position < len(self._current_playlist) - 1:
            self._playlist_position += 1
            song_id = self._current_playlist[self._playlist_position]
            song_data = self.db_access.songs.query_id(song_id)
            self.queue_song(song_data[2])
            self.next()

    def last(self) -> None:
        if self._timeline_position == 1:
            return
        self._timeline_position -= 1
        self._reload_playback()

    def queue_song(self, song_path: str) -> None:
        self._timeline.append(song_path)

    def set_playlist(self, playlist_id: int, playlist_position: int) -> None:
        playlist_data = self.db_access.playlists.query_id(playlist_id)
        self._current_playlist = playlist_data[3].split(",")
        self._playlist_position = playlist_position

    @property
    def song_position(self) -> float:
        """
        Position in the song in seconds.
        """
        return self.player.position

    @song_position.setter
    def song_position(self, position: float) -> None:
        self.player.position = position

    @property
    def song_length(self) -> float:
        try:
            audio = File(self._timeline[self._timeline_position - 1])
            return audio.info.length
        except IndexError:
            return 0
