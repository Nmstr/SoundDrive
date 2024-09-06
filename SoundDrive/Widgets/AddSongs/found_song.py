from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import QFile
from tinytag import TinyTag

class FoundSong(QFrame):
    def __init__(self, parent = None, song_path: str = None) -> None:
        super().__init__(parent)
        self.setObjectName("FoundSong")
        self.parent = parent
        self.song_path = song_path

        tag = TinyTag.get(self.song_path)
        try:
            song_title = tag.title
            song_artist = tag.artist
        except AttributeError:
            song_title = None
            song_artist = None

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("Widgets/AddSongs/found_song.ui")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Set size
        self.setMinimumSize(200, 100)
        self.setMaximumSize(1000, 100)

        self.ui.song_path_edit_label.setText(self.song_path)
        self.ui.song_name_input.setText(song_title)
        self.ui.artists_input.setText(song_artist)
