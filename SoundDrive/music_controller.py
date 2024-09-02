import PySoundSphere

class MusicController:
    def __init__(self, db_access):
        self.player = PySoundSphere.AudioPlayer("pygame")
        self.player.volume = 0.075
        self.db_access = db_access

    def play(self) -> None:
        self.player.play()

    def stop(self) -> None:
        self.player.pause()

    def last(self) -> None:
        self.next()

    def next(self) -> None:
        all_songs = self.db_access.songs.query()
        import random
        song = random.choice(all_songs)
        self.player.stop()
        self.player.load(song[2])
        self.player.play()
