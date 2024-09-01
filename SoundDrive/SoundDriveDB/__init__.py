from . import songs as _songs
from . import db as _db

class SoundDriveDB:
    def __init__(self):
        self.songs = _songs
        self.db = _db
