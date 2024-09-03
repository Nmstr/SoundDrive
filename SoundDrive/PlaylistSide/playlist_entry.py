from PySide6.QtWidgets import QFrame
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QFile

class PlaylistEntry(QFrame):
    def __init__(self, parent = None, playlist_data: str = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.playlist_data = playlist_data

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("PlaylistSide/playlist_entry.ui")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.ui.name_label.setText(self.playlist_data[1])

    def mousePressEvent(self, event):  # noqa: N802
        if event.button() == Qt.LeftButton:
            self.parent.set_page(3)
            self.show_playlist_data()
        return super().mousePressEvent(event)

    def show_playlist_data(self) -> None:
        ui = self.parent.ui
        ui.playlist_name_label.setText(self.playlist_data[1])
