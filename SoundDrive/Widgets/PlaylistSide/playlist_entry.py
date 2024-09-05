from PlaylistTab.song_entry import SongEntry
from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QFile

class PlaylistEntry(QFrame):
    def __init__(self, parent = None, playlist_data: str = None) -> None:
        super().__init__(parent)
        self.setObjectName("PlaylistEntry")
        self.parent = parent
        self.playlist_data = playlist_data

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("Widgets/PlaylistSide/playlist_entry.ui")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.ui.name_label.setText(self.playlist_data[1])

    def mousePressEvent(self, event):  # noqa: N802
        if event.button() == Qt.LeftButton:
            self.parent.set_page(3)
            self.show_playlist_data()
            self.parent.current_playlist = self.playlist_data[0]
        return super().mousePressEvent(event)

    def show_playlist_data(self) -> None:
        ui = self.parent.ui
        ui.playlist_name_label.setText(self.playlist_data[1])

        layout = self.parent.clear_field(self.parent.ui.playlist_songs_scroll_content, QVBoxLayout())
        if self.playlist_data[3] is None:
            return
        songs = self.playlist_data[3].split(",")
        for i, song in enumerate(songs):  # Dynamically add custom Widgets for each song in the playlist
            song_data = self.parent.db_access.songs.query_id(song)
            result = SongEntry(self, song_data, i)
            layout.addWidget(result)
