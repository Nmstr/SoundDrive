from . import playlists as _playlists
from . import songs as _songs
from . import db as _db
from .search import SearchEngine
from .config import Config

class SoundDriveDB:
    def __init__(self) -> None:
        self.playlists = _playlists
        self.songs = _songs
        self.db = _db
        self.search = SearchEngine()
        self.config = Config()
