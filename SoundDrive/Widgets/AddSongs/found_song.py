from PySide6.QtWidgets import QFrame, QLabel, QLineEdit, QGridLayout, QWidget
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

        ### --- This doesn't use a .ui file because it wouldn't resize horizontally ---- ###
        # Todo: Figure out "Why?" and change it
        self.ui = QWidget(self)
        self.ui.layout = QGridLayout(self)
        # Song path
        self.ui.song_path_info = QLabel("Song Path:", self)
        self.ui.layout.addWidget(self.ui.song_path_info, 0, 0)
        self.ui.song_path_edit_label = QLabel(self)
        self.ui.layout.addWidget(self.ui.song_path_edit_label, 0, 1)
        # Song name
        self.ui.song_name_label = QLabel("Song Name:", self)
        self.ui.layout.addWidget(self.ui.song_name_label, 1, 0)
        self.ui.song_name_input = QLineEdit(self)
        self.ui.layout.addWidget(self.ui.song_name_input, 1, 1)
        # Artists
        self.ui.artists_label = QLabel("Artists:", self)
        self.ui.layout.addWidget(self.ui.artists_label, 2, 0)
        self.ui.artists_input = QLineEdit(self)
        self.ui.layout.addWidget(self.ui.artists_input, 2, 1)
        ### --- ###

        self.ui.song_path_edit_label.setText(self.song_path)
        self.ui.song_name_input.setText(song_title)
        self.ui.artists_input.setText(song_artist)
