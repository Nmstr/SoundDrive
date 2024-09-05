from PySide6.QtWidgets import QFrame, QMenu
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QFile

class SearchResult(QFrame):
    def __init__(self, parent = None, song_data: str = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.song_data = song_data

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("SearchResult/search_result.ui")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.ui.name_label.setText(self.song_data[1])
        self.ui.path_label.setText(self.song_data[2])

    def mousePressEvent(self, event):  # noqa: N802
        if event.button() == Qt.LeftButton:
            self.parent.music_controller.play(self.song_data[2])
        return super().mousePressEvent(event)

    def contextMenuEvent(self, event):  # noqa: N802
        context_menu = QMenu(self)
        queue_action = context_menu.addAction("Queue Song")

        add_to_playlist_menu = QMenu("Add To Playlist", self)
        all_playlists = self.parent.db_access.playlists.query()
        for playlist in all_playlists:  # Dynamically add an action for each playlist
            playlist_action = add_to_playlist_menu.addAction(playlist[1])
            playlist_action.triggered.connect(lambda checked, p=playlist[0]: self.add_song_to_playlist(p))
        context_menu.addMenu(add_to_playlist_menu)

        # Connect actions to slots
        queue_action.triggered.connect(self.queue_song)

        context_menu.exec_(self.mapToGlobal(event.pos()))

    def queue_song(self):
        self.parent.music_controller.queue_song(self.song_data[2])

    def add_song_to_playlist(self, playlist_id):
        self.parent.db_access.playlists.add_song(playlist_id, self.song_data[0])
        self.parent.populate_playlists()
