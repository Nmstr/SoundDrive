from PySide6.QtWidgets import QFrame, QLabel, QLineEdit, QGridLayout, QWidget
from tinytag import TinyTag

class FoundSong(QFrame):
    def __init__(self, parent: object = None, song_path: str = None) -> None:
        super().__init__(parent)
        self.setObjectName("FoundSong")
        self.parent = parent
        self.song_path = song_path

        tag = TinyTag.get(self.song_path)
        try:
            self.song_title = tag.title
            self.song_artist = tag.artist
        except AttributeError:
            self.song_title = None
            self.song_artist = None

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
        self.ui.song_name_input.setText(self.song_title)
        self.ui.artists_input.setText(self.song_artist)

    def retrieve_final_data(self) -> list[str]:
        """
        Retrieves song title, path and artists from widget
        :return: The title, path and artists
        """
        return [self.song_title, self.song_path, self.song_artist]
