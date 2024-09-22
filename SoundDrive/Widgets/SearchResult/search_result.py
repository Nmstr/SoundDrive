from Widgets.song_icon import SongIcon
from PySide6.QtWidgets import QFrame, QMenu
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QFile

class SearchResult(QFrame):
    def __init__(self, parent: object = None, song_data: str = None) -> None:
        super().__init__(parent)
        self.setObjectName("SearchResult")
        self.parent = parent
        self.song_data = song_data

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("Widgets/SearchResult/search_result.ui")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Add song icon
        song_icon = SongIcon(self, self.parent.get_img_cover, self.song_data)
        self.ui.song_icon_container.layout().addWidget(song_icon)

        # Set size
        self.setMinimumSize(200, 200)
        self.setMaximumSize(1000, 200)

        self.ui.name_label.setText(self.song_data[1])
        self.ui.path_label.setText(self.song_data[2])

    def mousePressEvent(self, event) -> None:  # noqa: N802
        """
        Start playing the song
        """
        if event.button() == Qt.LeftButton:
            self.parent.music_controller.play(self.song_data[2])
        return super().mousePressEvent(event)

    def contextMenuEvent(self, event) -> None:  # noqa: N802
        """
        Show context menu
        :return: None
        """
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

    def queue_song(self) -> None:
        """
        Queue the song
        :return: None
        """
        self.parent.music_controller.queue_song(self.song_data[2])

    def add_song_to_playlist(self, playlist_id: int) -> None:
        """
        Adds the song to a playlist
        :param playlist_id: The id of the playlist the song should be added to
        :return: None
        """
        self.parent.db_access.playlists.add_song(playlist_id, self.song_data[0])
        self.parent.populate_playlists()
