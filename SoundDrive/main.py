from PlaylistSide.playlist_entry import PlaylistEntry
from SearchResult.search_result import SearchResult
from MenuButton.menu_button import MenuButton
from music_controller import MusicController
from SoundDriveDB import SoundDriveDB
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import sys
import os

MUSIC_DIR = os.path.abspath("../music")

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SoundDrive")

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("main.ui")
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setGeometry(self.ui.geometry())
        self.showMaximized()

        # Access db
        self.db_access = SoundDriveDB()
        self.db_access.db.create_db()

        # Create player
        self.music_controller = MusicController()

        # Create menu buttons
        self.add_menu_button("home")
        self.add_menu_button("library")
        self.add_menu_button("search")

        # Connect buttons
        self.ui.play_btn.clicked.connect(lambda: self.music_controller.continue_playback())
        self.ui.stop_btn.clicked.connect(lambda: self.music_controller.stop())
        self.ui.last_btn.clicked.connect(lambda: self.music_controller.last())
        self.ui.next_btn.clicked.connect(lambda: self.music_controller.next())
        self.ui.add_songs_btn.clicked.connect(self.add_songs)

        self.ui.search_bar.textChanged.connect(self.search)

        self.populate_playlists()

    def search(self, text: str) -> None:
        print(text)
        layout = self.clear_field(self.ui.search_scroll_content, QVBoxLayout())

        # Dynamically add custom widgets for each song
        all_songs = self.db_access.songs.query()
        for song in all_songs:
            result = SearchResult(self, song)
            layout.addWidget(result)

    def populate_playlists(self):
        layout = self.clear_field(self.ui.playlist_scroll_content, QVBoxLayout())

        # Dynamically add custom widgets for each song
        all_playlists = self.db_access.playlists.query()
        for playlist in all_playlists:
            result = PlaylistEntry(self, playlist)
            layout.addWidget(result)

    def clear_field(self, container, target_layout):
        # Check if the container has a layout, if not, set a new layout of type target_layout
        layout = container.layout()
        if layout is None:
            layout = target_layout
            container.setLayout(layout)

        # Clear existing content in the layout
        for i in reversed(range(layout.count())):
            layout_item = layout.itemAt(i)
            if layout_item.widget() is not None:
                layout_item.widget().deleteLater()

        return layout

    def add_songs(self) -> None:
        all_songs = os.listdir(MUSIC_DIR)
        for song in all_songs:
            self.db_access.songs.create(song, os.path.join(MUSIC_DIR, song))

    def add_menu_button(self, button_type: str) -> None:
        layout = self.ui.menu.layout()
        self.frame = MenuButton(self, button_type)
        layout.addWidget(self.frame)
        self.setLayout(layout)

    def set_page(self, page_number: int) -> None:
        self.ui.page.setCurrentIndex(page_number)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
