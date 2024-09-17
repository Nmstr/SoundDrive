from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import QFile

class SongActions(QFrame):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setObjectName("SongActions")
        self.parent = parent

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("Widgets/AddSongs/song_actions.ui")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.ui.add_songs_confirm_btn.clicked.connect(lambda: self.confirm_add_song())

    def confirm_add_song(self):
        for found_song in self.parent.found_song_widgets:
            found_song_data = found_song.retrieve_final_data()
            self.parent.db_access.songs.create(found_song_data[0], found_song_data[1], found_song_data[2])
        self.parent.set_page(0)
        self.parent.db_access.search.create_index_thread()
