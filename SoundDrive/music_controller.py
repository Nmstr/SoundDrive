import PySoundSphere

class MusicController:
    def __init__(self):
        self.player = PySoundSphere.AudioPlayer("pygame")
        self.player.volume = 0.075
        self._timeline = []
        self._timeline_position = 0

    def _reload_playback(self):
        self.player.load(self._timeline[self._timeline_position - 1])
        self.player.stop()
        self.player.play()

    def play(self, song_path: str):
        self._timeline = self._timeline[:self._timeline_position]
        self._timeline_position += 1
        self._timeline.append(song_path)
        self._reload_playback()

    def continue_playback(self):
        self.player.play()

    def stop(self):
        self.player.pause()

    def next(self):
        if self._timeline_position < len(self._timeline):
            self._timeline_position += 1
            self._reload_playback()

    def last(self):
        if self._timeline_position == 1:
            return
        self._timeline_position -= 1
        self._reload_playback()

    def queue_song(self, song_path):
        self._timeline.append(song_path)
