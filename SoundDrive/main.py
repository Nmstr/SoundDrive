from Dialogs.delete_playlist_dialog import DeletePlaylistDialog
from Widgets.PlaylistSide.playlist_entry import PlaylistEntry
from Widgets.SearchResult.search_result import SearchResult
from Widgets.MenuButton.menu_button import MenuButton
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
        self.setObjectName("MainWindow")
        self.setWindowTitle("SoundDrive")
        self.current_playlist = None

        # Load the stylesheet
        with open('style.qss', 'r') as f:
            app.setStyleSheet(f.read())
            pass

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
        self.music_controller = MusicController(self.db_access)

        # Create menu buttons
        self.add_menu_button("home")
        self.add_menu_button("library")
        self.add_menu_button("search")

        # Connect buttons
        self.ui.play_btn.clicked.connect(lambda: self.music_controller.continue_playback())
        self.ui.stop_btn.clicked.connect(lambda: self.music_controller.stop())
        self.ui.last_btn.clicked.connect(lambda: self.music_controller.last())
        self.ui.next_btn.clicked.connect(lambda: self.music_controller.next())
        self.ui.add_songs_btn.clicked.connect(lambda: self.add_songs())
        self.ui.create_playlist_btn.clicked.connect(lambda: self.create_playlist())
        self.ui.delete_playlist_btn.clicked.connect(lambda: self.delete_playlist())

        self.ui.search_bar.textChanged.connect(self.search)

        self.populate_playlists()

        from Widgets.time_slider import TimeSlider
        layout = self.ui.time_slider_container.layout()
        self.timeSlider = TimeSlider(self)
        layout.addWidget(self.timeSlider)

    def search(self, text: str) -> None:
        print(text)
        layout = self.clear_field(self.ui.search_scroll_content, QVBoxLayout())

        # Dynamically add custom Widgets for each song
        all_songs = self.db_access.songs.query()
        for song in all_songs:
            result = SearchResult(self, song)
            layout.addWidget(result)

    def populate_playlists(self):
        layout = self.clear_field(self.ui.playlist_scroll_content, QVBoxLayout())

        # Dynamically add custom Widgets for each song
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

    def create_playlist(self):
        self.db_access.playlists.create()
        self.populate_playlists()

    def delete_playlist(self):
        dlg = DeletePlaylistDialog(self.db_access, self.current_playlist)
        if dlg.exec():
            self.db_access.playlists.delete(self.current_playlist)

        self.populate_playlists()

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
