from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import QFile

class SongActions(QFrame):
    def __init__(self, parent: object = None) -> None:
        super().__init__(parent)
        self.setObjectName("SongActions")
        self.parent = parent

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("Widgets/AddSongs/song_actions.ui")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.ui.add_songs_confirm_btn.clicked.connect(lambda: self.parent.new_song_manager.confirm_add_song())
