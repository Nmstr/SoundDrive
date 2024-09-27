from Widgets.Playlist.song_entry import SongEntry
from Widgets.Playlist.playlist_icon import PlaylistIcon
from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QFile
from tinytag import TinyTag

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
        # Display playlist icon (on itself)
        side_layout = self.parent.clear_field(self.ui.playlist_icon_container, QVBoxLayout(), amount_left=0)
        size = (self.ui.playlist_icon_container.width(), self.ui.playlist_icon_container.height())
        song_icon = PlaylistIcon(self, self.playlist_data, size = size)
        side_layout.addWidget(song_icon)

        # Set size
        self.setMinimumSize(200, 100)
        self.setMaximumSize(1000, 100)

    def mousePressEvent(self, event):  # noqa: N802
        """
        Execute the activate function on left click
        """
        if event.button() == Qt.LeftButton:
            self.activate()
        return super().mousePressEvent(event)

    def activate(self) -> None:
        """
        Set the page to the playlist page, display the playlist data and change the current playlist of the parent
        This was previously inside mousePressEvent; it was moved because it needs to be called from song_entry
        :return: None
        """
        self.parent.set_page(3)
        self.show_playlist_data()
        self.parent.current_playlist = self.playlist_data[0]

    def show_playlist_data(self) -> None:
        """
        Update the ui with the playlist data
        :return: None
        """
        self.parent.ui.playlist_name_label.setText(self.playlist_data[1])
        playlist_length = 0

        # Display songs
        content_layout = self.parent.clear_field(self.parent.ui.playlist_songs_scroll_content, QVBoxLayout())
        if self.playlist_data[3] is not None:
            songs = self.playlist_data[3].split(",")
            for i, song in enumerate(songs):  # Dynamically add custom Widgets for each song in the playlist
                song_data = self.parent.db_access.songs.query_id(song)
                song_entry = SongEntry(self, song_data, i)
                content_layout.insertWidget(content_layout.count() - 1, song_entry)
                playlist_length += TinyTag.get(song_data[2]).duration  # Also count total length of playlist for later

        # Display playlist icon (in content page)
        side_layout = self.parent.clear_field(self.parent.ui.playlist_icon_container, QVBoxLayout(), amount_left=0)
        song_icon = PlaylistIcon(self, self.playlist_data, size = (200, 200))
        side_layout.addWidget(song_icon)

        if self.playlist_data[3]:
            # Display number songs
            self.parent.ui.playlist_song_number_label.setText(str(len(self.playlist_data[3].split(","))) + " songs")
            # Display playlist length
            hours = int(playlist_length // 3600)
            minutes = int((playlist_length % 3600) // 60)
            self.parent.ui.playlist_total_length_label.setText(f"{hours} hr {minutes} min")
        else:
            # Reset labels
            self.parent.ui.playlist_song_number_label.setText("0 songs")
            self.parent.ui.playlist_total_length_label.setText("0 hr 0 min")
