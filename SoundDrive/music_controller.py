from tinytag import TinyTag
import PySoundSphere

class MusicController:
    def __init__(self, parent: object) -> None:
        self.player = PySoundSphere.AudioPlayer("pygame")
        self.player.set_callback_function(self.next)
        self.player.volume = 0.075
        self.parent = parent
        self._timeline = []
        self._timeline_position = 0
        self._current_playlist = None
        self._playlist_position = 0
        self.is_playing = False

    def _reload_playback(self) -> None:
        """
        Reload the playback by

        - loading a new song
        - stopping the playback
        - starting the playback
        :return: None
        """
        self.player.load(self._timeline[self._timeline_position - 1])
        self.player.stop()
        self.player.play()
        self.parent.set_current_song_data(self._timeline[self._timeline_position - 1])

    def play(self, song_path: str) -> None:
        """
        Add a song to the timeline and play it
        :param song_path: The path of the song to play
        :return: None
        """
        self._timeline = self._timeline[:self._timeline_position]
        self._timeline_position += 1
        self._timeline.append(song_path)
        self._reload_playback()
        self.is_playing = True
        self.parent.play_pause_btn.update()

    def continue_playback(self) -> None:
        """
        Unpause playback
        :return: None
        """
        self.player.play()
        self.is_playing = True
        self.parent.play_pause_btn.update()

    def stop(self) -> None:
        """
        Stop playback
        :return: None
        """
        self.player.pause()
        self.is_playing = False
        self.parent.play_pause_btn.update()

    def next(self) -> None:
        """
        Play the next song from the timeline
        :return: None
        """
        if self._timeline_position < len(self._timeline):
            self._timeline_position += 1
            self._reload_playback()
        elif self._current_playlist is not None and self._playlist_position < len(self._current_playlist) - 1:
            self._playlist_position += 1
            song_id = self._current_playlist[self._playlist_position]
            song_data = self.parent.db_access.songs.query_id(song_id)
            self.queue_song(song_data[2])
            self.next()

    def last(self) -> None:
        """
        Play the previous song from the timeline
        :return: None
        """
        if self._timeline_position == 1:
            return
        self._timeline_position -= 1
        self._reload_playback()

    def queue_song(self, song_path: str) -> None:
        """
        Queue song at the end of the timeline
        :param song_path: The path of the song to queue
        :return: None
        """
        self._timeline.append(song_path)

    def set_playlist(self, playlist_id: int, playlist_position: int) -> None:
        """
        Set the playlist currently playing
        :param playlist_id: The id of the playlist
        :param playlist_position: The position inside the playlist
        :return: None
        """
        playlist_data = self.parent.db_access.playlists.query_id(playlist_id)

        # Remove deleted songs from playlist
        new_playlist_ids = []
        playlist_song_ids = playlist_data[3].split(",")
        for playlist_song_id in playlist_song_ids:
            song_data = self.parent.db_access.songs.query_id(playlist_song_id)
            if song_data[4] == 0:
                new_playlist_ids.append(song_data[0])

        self._current_playlist = new_playlist_ids
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
    def volume(self) -> float:
        """
        Volume between 0 and 1.
        """
        return self.player.volume

    @volume.setter
    def volume(self, volume: float) -> None:
        self.player.volume = volume

    @property
    def song_length(self) -> float:
        """
        The length of the song
        """
        try:
            tag = TinyTag.get(self._timeline[self._timeline_position - 1])
            return tag.duration
        except IndexError:
            return 0
