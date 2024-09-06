from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, QFile

class FoundSong(QFrame):
    def __init__(self, parent = None, song_data: str = None) -> None:
        super().__init__(parent)
        self.setObjectName("FoundSong")
        self.parent = parent
        self.song_data = song_data
        print(self.song_data)

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("Widgets/AddSongs/found_song.ui")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Set size
        self.setMinimumSize(200, 100)
        self.setMaximumSize(1000, 100)

    def mousePressEvent(self, event):  # noqa: N802
        if event.button() == Qt.LeftButton:
            pass
        return super().mousePressEvent(event)
