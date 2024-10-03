from . import playlists as _playlists
from . import artists as _artists
from . import songs as _songs
from . import db as _db
from .search import SearchEngine
from .config import Config
from .stats import Stats

class SoundDriveDB:
    def __init__(self) -> None:
        self.playlists = _playlists
        self.artists = _artists
        self.songs = _songs
        self.db = _db
        self.search = SearchEngine()
        self.config = Config()
        self.stats = Stats()
