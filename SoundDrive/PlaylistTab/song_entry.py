from PySide6.QtWidgets import QFrame, QMenu
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QFile

class SongEntry(QFrame):
    def __init__(self, parent = None, song_data: str = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.song_data = song_data

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("PlaylistTab/song_entry.ui")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.ui.name_label.setText(self.song_data[1])
        self.ui.path_label.setText(self.song_data[2])

    def mousePressEvent(self, event):  # noqa: N802
        if event.button() == Qt.LeftButton:
            self.parent.parent.music_controller.play(self.song_data[2])
        return super().mousePressEvent(event)
