from . import playlists as _playlists
from . import songs as _songs
from . import db as _db
from .search import SearchEngine

class SoundDriveDB:
    def __init__(self):
        self.playlists = _playlists
        self.songs = _songs
        self.db = _db
        self.search = SearchEngine()
