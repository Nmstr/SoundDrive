from PySide6.QtWidgets import QFrame
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QFile

class SongEntry(QFrame):
    def __init__(self, parent = None, song_data: str = None, song_index: int = None) -> None:
        super().__init__(parent)
        self.setObjectName("SongEntry")
        self.parent = parent
        self.song_data = song_data
        self.song_index = song_index

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("Widgets/SongEntry/song_entry.ui")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.ui.name_label.setText(self.song_data[1])
        self.ui.path_label.setText(self.song_data[2])

        # Set size
        self.setMinimumSize(200, 200)
        self.setMaximumSize(1000, 200)

    def mousePressEvent(self, event):  # noqa: N802
        if event.button() == Qt.LeftButton:
            self.parent.parent.music_controller.play(self.song_data[2])
            self.parent.parent.music_controller.set_playlist(self.parent.playlist_data[0], self.song_index)
        return super().mousePressEvent(event)
