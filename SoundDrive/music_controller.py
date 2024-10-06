from tinytag import TinyTag
import PySoundSphere

class MusicController:
    def __init__(self, parent: object) -> None:
        self.parent = parent
        self._player = PySoundSphere.AudioPlayer("pygame")
        self._player.volume = 0.05
        self._current_playlist = []
        self._playlist_position = 0
        self._queue = []
        self.is_playing = False

    def _reload_playback(self, song_id: int = None) -> None:
        """
        Reload the playback
        :param song_id: Overwrite for when not to use the next song from the playlist. Plays the song specified using its id instead. Use with caution.
        :return: None
        """
        if song_id:  # Song id was supplied
            song_path = self.parent.db_access.songs.query_id(song_id)[2]
            self.parent.update_song_data_signal.emit(str(song_id))
        else:  # Song id wasn't supplied (next from playlist)
            song_path = self.parent.db_access.songs.query_id(self._current_playlist[self._playlist_position])[2]
            self.parent.update_song_data_signal.emit(self._current_playlist[self._playlist_position])
        self._player.load(song_path)
        self._player.stop()
        self._player.play()
        self.is_playing = True
        self.parent.play_pause_btn.update()

    def play_playlist(self, playlist_id: int, position: int) -> None:
        """
        Plays a playlist
        :param playlist_id: The id of the playlist to be played
        :param position: The position in the playlist
        :return: None
        """
        playlist_data = self.parent.db_access.playlists.query_id(playlist_id)
        self._current_playlist = playlist_data[3].split(",")
        self._playlist_position = position
        self._reload_playback()

    def play_song(self, song_id: int) -> None:
        """
        Plays a song by pretending it is a playlist with 1 element
        :param song_id: The id of the song
        :return: None
        """
        self._current_playlist = [str(song_id)]
        self._playlist_position = 0
        self._reload_playback()

    def next(self) -> None:
        """
        Play the next song from the playlist
        :return: None
        """
        if len(self._queue) > 0:
            self._reload_playback(self._queue.pop(0))
        elif self._playlist_position < len(self._current_playlist) - 1:
            self._playlist_position += 1
            self._reload_playback()

    def last(self) -> None:
        """
        Play the previous song from the playlist
        :return: None
        """
        if self._playlist_position == 0:
            return
        self._playlist_position -= 1
        self._reload_playback()

    def unpause(self) -> None:
        """
        Unpause playback
        :return: None
        """
        self._player.play()
        self.is_playing = True
        self.parent.play_pause_btn.update()

    def pause(self) -> None:
        """
        Pause playback
        :return: None
        """
        self._player.pause()
        self.is_playing = False
        self.parent.play_pause_btn.update()

    def queue_song(self, song_id: int) -> None:
        """
        Adds a song to the queue
        :param song_id: The id of the song to be added
        :return: None
        """
        self._queue.append(song_id)

    @property
    def song_position(self) -> float:
        """
        Position in the current playing song in seconds.
        """
        return self._player.position

    @song_position.setter
    def song_position(self, position: float) -> None:
        self._player.position = position

    @property
    def song_length(self) -> float:
        """
        The length of the current playing song in seconds
        """
        try:
            song_path = self.parent.db_access.songs.query_id(self._current_playlist[self._playlist_position])[2]
            tag = TinyTag.get(song_path)
            return tag.duration
        except IndexError:
            return 0

    @property
    def volume(self) -> float:
        """
        Volume between 0 and 1.
        """
        return self._player.volume

    @volume.setter
    def volume(self, volume: float) -> None:
        self._player.volume = volume
