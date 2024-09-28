from Widgets.song_icon import SongIcon
from PySide6.QtWidgets import QFrame, QMenu
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QFile

class SongEntry(QFrame):
    def __init__(self, parent: object = None, song_data: str = None, song_index: int = None) -> None:
        super().__init__(parent)
        self.setObjectName("SongEntry")
        self.parent = parent
        self.song_data = song_data
        self.song_index = song_index

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("Widgets/Playlist/song_entry.ui")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.ui.name_label.setText(self.song_data[1])
        self.ui.path_label.setText(self.song_data[2])

        # Add song icon
        song_icon = SongIcon(self, self.song_data)
        self.ui.song_icon_container.layout().addWidget(song_icon)

        if song_data[4] == 1:
            self.setDisabled(True)

        # Set size
        self.setMinimumSize(200, 200)
        self.setMaximumSize(1000, 200)

    def mousePressEvent(self, event):  # noqa: N802
        """
        Start playing the song and set the playlist
        """
        if event.button() == Qt.LeftButton:
            self.parent.parent.music_controller.play(self.song_data[2])
            self.parent.parent.music_controller.set_playlist(self.parent.playlist_data[0], self.song_index)
        return super().mousePressEvent(event)

    def contextMenuEvent(self, event) -> None:  # noqa: N802
        """
        Show context menu
        :return: None
        """
        context_menu = QMenu(self)
        queue_action = context_menu.addAction("Queue Song")
        remove_action = context_menu.addAction("Remove From Playlist")

        add_to_playlist_menu = QMenu("Add To Playlist", self)
        all_playlists = self.parent.parent.db_access.playlists.query()
        for playlist in all_playlists:  # Dynamically add an action for each playlist
            playlist_action = add_to_playlist_menu.addAction(playlist[1])
            playlist_action.triggered.connect(lambda checked, p=playlist[0]: self.add_song_to_playlist(p))
        context_menu.addMenu(add_to_playlist_menu)

        # Connect actions to slots
        queue_action.triggered.connect(self.queue_song)
        remove_action.triggered.connect(self.remove_song)

        context_menu.exec_(self.mapToGlobal(event.pos()))

    def queue_song(self) -> None:
        """
        Queue the song
        :return: None
        """
        self.parent.parent.music_controller.queue_song(self.song_data[2])

    def remove_song(self) -> None:
        """
        Removes the song from the playlist
        :return: None
        """
        self.parent.parent.db_access.playlists.remove_song(self.parent.playlist_data[0], self.song_index)
        self.parent.parent.populate_playlists()
        self.parent.parent.playlist_dict[self.parent.playlist_data[0]].activate()

    def add_song_to_playlist(self, playlist_id: int) -> None:
        """
        Adds the song to a playlist
        :param playlist_id: The id of the playlist the song should be added to
        :return: None
        """
        self.parent.parent.db_access.playlists.add_song(playlist_id, self.song_data[0])
        self.parent.parent.populate_playlists()
        self.parent.parent.playlist_dict[self.parent.playlist_data[0]].activate()
