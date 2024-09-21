from Dialogs.add_remove_music_dir_dialog import AddRemoveMusicDirDialog
from Dialogs.delete_playlist_dialog import DeletePlaylistDialog
from Widgets.generic_control_button import GenericControlButton
from Widgets.PlaylistSide.playlist_entry import PlaylistEntry
from Widgets.SearchResult.search_result import SearchResult
from Widgets.MenuButton.menu_button import MenuButton
from Widgets.play_pause_button import PlayPauseButton
from Widgets.volume_slider import VolumeSlider
from Widgets.time_slider import TimeSlider
from functions.add_songs import NewSongManager
from music_controller import MusicController
from SoundDriveDB import SoundDriveDB
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from tinytag import TinyTag
from io import BytesIO
from PIL import Image
import pickle
import PIL
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("SoundDrive")
        self.current_playlist = None
        self.found_song_widgets = []

        # Load the stylesheet
        with open('style.qss', 'r') as f:
            app.setStyleSheet(f.read())

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
        self.new_song_manager = NewSongManager(self)
        self.db_access.songs.hash_db()

        # Create player
        self.music_controller = MusicController(self)

        # Create menu buttons
        self.add_menu_button("home")
        self.add_menu_button("library")
        self.add_menu_button("search")
        self.add_menu_button("settings")

        # Connect buttons
        self.ui.add_songs_btn.clicked.connect(lambda: self.new_song_manager.add_songs())
        self.ui.create_playlist_btn.clicked.connect(lambda: self.create_playlist())
        self.ui.delete_playlist_btn.clicked.connect(lambda: self.delete_playlist())
        self.ui.add_music_dir_btn.clicked.connect(lambda: self.add_music_dir())
        self.ui.remove_music_dir_btn.clicked.connect(lambda: self.remove_music_dir())

        self.ui.search_bar.textChanged.connect(self.search)

        self.populate_playlists()
        self.populate_control_bar()
        self.populate_settings_music_dir()

    def search(self, text: str) -> None:
        print(text)

        # Query the requested input
        song_ids =  self.db_access.search.query(text)
        all_songs = []
        for song_id in song_ids:
            all_songs.append(self.db_access.songs.query_id(song_id))

        # Dynamically add custom Widgets for each song
        layout = self.clear_field(self.ui.search_scroll_content, QVBoxLayout())
        for song in all_songs:
            result = SearchResult(self, song)
            layout.insertWidget(layout.count() - 1, result)

    def populate_playlists(self):
        layout = self.clear_field(self.ui.playlist_scroll_content, QVBoxLayout())

        # Dynamically add custom Widgets for each song
        all_playlists = self.db_access.playlists.query()
        for playlist in all_playlists:
            playlist_entry = PlaylistEntry(self, playlist)
            layout.insertWidget(layout.count() - 1, playlist_entry)

    def clear_field(self, container, target_layout, *, amount_left = 1):
        # Check if the container has a layout, if not, set a new layout of type target_layout
        layout = container.layout()
        if layout is None:
            layout = target_layout
            container.setLayout(layout)

        while layout.count() > amount_left:
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        return layout

    def populate_control_bar(self) -> None:
        def add_widget(container, widget):
            layout = container.layout()
            layout.addWidget(widget)

        # Create and add widgets
        self.time_slider = TimeSlider(self)
        add_widget(self.ui.time_slider_container, self.time_slider)

        self.volume_slider = VolumeSlider(self)
        add_widget(self.ui.volume_slider_container, self.volume_slider)

        self.play_pause_btn = PlayPauseButton(self)
        add_widget(self.ui.play_pause_btn_container, self.play_pause_btn)

        self.next_btn = GenericControlButton(self, "Assets/next.svg", lambda: self.music_controller.next())
        add_widget(self.ui.next_btn_container, self.next_btn)

        self.last_btn = GenericControlButton(self, "Assets/last.svg", lambda: self.music_controller.last())
        add_widget(self.ui.last_btn_container, self.last_btn)

    def populate_settings_music_dir(self):
        layout = self.clear_field(self.ui.music_dir_frame, QVBoxLayout(), amount_left=0)
        for this_dir in self.db_access.config.get_music_dirs():
            dir_label = QLabel(self)
            dir_label.setText(this_dir)
            layout.addWidget(dir_label)

    def create_playlist(self):
        self.db_access.playlists.create()
        self.populate_playlists()

    def delete_playlist(self):
        dlg = DeletePlaylistDialog(self.db_access, self.current_playlist)
        if dlg.exec():
            self.db_access.playlists.delete(self.current_playlist)

        self.populate_playlists()

    def add_music_dir(self):
        dlg = AddRemoveMusicDirDialog(dialog_type="add")
        if dlg.exec():
            self.db_access.config.add_music_dir(dlg.edit.text())
            self.populate_settings_music_dir()

    def remove_music_dir(self):
        dlg = AddRemoveMusicDirDialog(dialog_type="remove")
        if dlg.exec():
            self.db_access.config.remove_music_dir(dlg.edit.text())
            self.populate_settings_music_dir()

    def add_menu_button(self, button_type: str) -> None:
        layout = self.ui.menu.layout()
        self.frame = MenuButton(self, button_type)
        layout.addWidget(self.frame)
        self.setLayout(layout)

    def set_page(self, page_number: int) -> None:
        self.ui.page.setCurrentIndex(page_number)

    def get_img_cover(self, file_path: str, *, resolution: tuple = (150, 150)) -> bytes | bool:
        cache_dir = os.getenv('XDG_CACHE_HOME', default=os.path.expanduser('~/.cache') + '/SoundDrive/covers/')
        cache_path = cache_dir + os.path.basename(file_path) + str(resolution) + '.cache'
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        # Check if the image data is cached and return
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                img_data = pickle.load(f)
            return img_data

        # Load the image
        tag = TinyTag.get(file_path, image=True)
        img_data = tag.get_image()

        # Resize the image
        try:
            image = Image.open(BytesIO(img_data))
            image = image.resize(resolution, Image.LANCZOS)
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_data = img_byte_arr.getvalue()
        except PIL.UnidentifiedImageError:
            return False

        # Cache the image data
        with open(cache_path, 'wb') as f:
            pickle.dump(img_data, f)
        return img_data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
