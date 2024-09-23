from Dialogs.add_remove_music_dir_dialog import AddRemoveMusicDirDialog
from Dialogs.delete_playlist_dialog import DeletePlaylistDialog
from Widgets.generic_control_button import GenericControlButton
from Widgets.PlaylistSide.playlist_entry import PlaylistEntry
from Widgets.SearchResult.search_result import SearchResult
from Widgets.MenuButton.menu_button import MenuButton
from Widgets.play_pause_button import PlayPauseButton
from Widgets.volume_slider import VolumeSlider
from Widgets.time_slider import TimeSlider
from Widgets.song_icon import SongIcon
from functions.add_songs import NewSongManager
from music_controller import MusicController
from SoundDriveDB import SoundDriveDB
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Signal
from PySide6.QtCore import QFile
from tinytag import TinyTag
from io import BytesIO
from PIL import Image
import pickle
import PIL
import sys
import os

class MainWindow(QMainWindow):
    update_song_data_signal = Signal(str)

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
        self.db_access.songs.check_db()

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
        # Connect signals
        self.update_song_data_signal.connect(self.set_current_song_data)

        self.ui.search_bar.textChanged.connect(self.search)

        self.populate_playlists()
        self.populate_control_bar()
        self.populate_settings_music_dir()

    def search(self, text: str) -> None:
        """
        Searches the database for songs matching the given query string.
        :param text: The query string to search within the database.
        :return: None. This method updates the UI with search results.
        """
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

    def populate_playlists(self) -> None:
        """
        Populates the left sidebar with the playlists from the db.
        :return: None
        """
        layout = self.clear_field(self.ui.playlist_scroll_content, QVBoxLayout())

        # Dynamically add custom Widgets for each song
        all_playlists = self.db_access.playlists.query()
        for playlist in all_playlists:
            playlist_entry = PlaylistEntry(self, playlist)
            layout.insertWidget(layout.count() - 1, playlist_entry)

    def clear_field(self, container: str, target_layout, *, amount_left: int = 1):
        """
        Clear a container of its contents
        :param container: The container to clear
        :param target_layout: The layout that should be added if none exists (e.g. QVboxLayout, QHboxLayout...)
        :param amount_left: The amount of elements that should be kept
        :return: None
        """
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
        """
        Populates the control bar with various control buttons and sliders.
        :return: None
        """
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

    def populate_settings_music_dir(self) -> None:
        """
        Populates the settings section with the music directories from the configuration.
        :return: None
        """
        layout = self.clear_field(self.ui.music_dir_frame, QVBoxLayout(), amount_left=0)
        for this_dir in self.db_access.config.get_music_dirs():
            dir_label = QLabel(self)
            dir_label.setText(this_dir)
            layout.addWidget(dir_label)

    def create_playlist(self) -> None:
        """
        Creates a playlist and updates the UI.
        :return: None
        """
        self.db_access.playlists.create()
        self.populate_playlists()

    def delete_playlist(self) -> None:
        """
        Deletes the selected playlist and updates the UI.
        Opens a dialog for confirmation
        :return: None
        """
        dlg = DeletePlaylistDialog(self.db_access, self.current_playlist)
        if dlg.exec():
            self.db_access.playlists.delete(self.current_playlist)

        self.populate_playlists()

    def add_music_dir(self) -> None:
        """
        Adds a music dir to the config and updates the UI
        :return: None
        """
        dlg = AddRemoveMusicDirDialog(dialog_type="add")
        if dlg.exec():
            self.db_access.config.add_music_dir(dlg.edit.text())
            self.populate_settings_music_dir()

    def remove_music_dir(self) -> None:
        """
        Removes a music dir from the config and updates the UI
        :return: None
        """
        dlg = AddRemoveMusicDirDialog(dialog_type="remove")
        if dlg.exec():
            self.db_access.config.remove_music_dir(dlg.edit.text())
            self.populate_settings_music_dir()

    def add_menu_button(self, button_type: str) -> None:
        """
        Adds a menu button
        :param button_type: The type of the button (e.g. search, settings)
        :return: None
        """
        layout = self.ui.menu.layout()
        self.frame = MenuButton(self, button_type)
        layout.addWidget(self.frame)
        self.setLayout(layout)

    def set_page(self, page_number: int) -> None:
        """
        Changes the current page in the main content field
        :param page_number: The number of the page to switch to
        :return: None
        """
        self.ui.page.setCurrentIndex(page_number)

    def get_img_cover(self, file_path: str, *, resolution: tuple = (150, 150)) -> bytes | bool:
        """
        Gets the cover of a song
        :param file_path: Path to the song
        :param resolution: The resolution the cover should have
        :return: Either the cover or a False
        """
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

    def set_current_song_data(self, song_path: str) -> None:
        """
        Sets song icon, name and path in bar
        :param song_path: The path of the song
        :return: None
        """
        layout = self.clear_field(self.ui.current_song_icon_container, QVBoxLayout(), amount_left=0)
        song_data = self.db_access.songs.query_path(song_path)
        song_icon = SongIcon(self, self.get_img_cover, song_data, size = (100, 100))
        layout.addWidget(song_icon)
        self.ui.current_song_name_label.setText(song_data[1])
        self.ui.current_song_artists_label.setText(song_data[3])

    def resizeEvent(self, event) -> None:  # noqa: N802
        """
        Executes on window resize and keeps music controls centered
        :return: None
        """
        half_window_width = self.size().width() / 2
        bar_left_width = self.ui.bar_left.size().width()
        half_bar_middle_width = self.ui.bar_middle.size().width() / 2
        spacer_width = half_window_width - bar_left_width - half_bar_middle_width
        if spacer_width < 0:
            spacer_width = 0
        self.ui.bar_left_middle_spacer_widget.setFixedSize(spacer_width, 100)
        return super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
