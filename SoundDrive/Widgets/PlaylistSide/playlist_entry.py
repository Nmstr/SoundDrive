from Widgets.Playlist.song_entry import SongEntry
from Widgets.Playlist.playlist_icon import PlaylistIcon
from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QFile

class PlaylistEntry(QFrame):
    def __init__(self, parent: object = None, playlist_data: str = None) -> None:
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

        # Set size
        self.setMinimumSize(200, 100)
        self.setMaximumSize(1000, 100)

    def mousePressEvent(self, event):  # noqa: N802
        """
        Set the main content page to the playlist page and fill in data
        """
        if event.button() == Qt.LeftButton:
            self.parent.set_page(3)
            self.show_playlist_data()
            self.parent.current_playlist = self.playlist_data[0]
        return super().mousePressEvent(event)

    def show_playlist_data(self) -> None:
        """
        Update the ui with the playlist data
        :return: None
        """
        self.parent.ui.playlist_name_label.setText(self.playlist_data[1])

        content_layout = self.parent.clear_field(self.parent.ui.playlist_songs_scroll_content, QVBoxLayout())
        if self.playlist_data[3] is None:
            return
        songs = self.playlist_data[3].split(",")
        for i, song in enumerate(songs):  # Dynamically add custom Widgets for each song in the playlist
            song_data = self.parent.db_access.songs.query_id(song)
            song_entry = SongEntry(self, song_data, i)
            content_layout.insertWidget(content_layout.count() - 1, song_entry)

        side_layout = self.parent.clear_field(self.parent.ui.playlist_icon_container, QVBoxLayout(), amount_left=0)
        song_icon = PlaylistIcon(self, self.playlist_data, size = (200, 200))
        side_layout.addWidget(song_icon)
