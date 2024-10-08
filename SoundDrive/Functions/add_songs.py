from Widgets.AddSongs.song_actions import SongActions
from Widgets.AddSongs.found_song import FoundSong
from PySide6.QtWidgets import QVBoxLayout, QLabel, QApplication
from PySide6.QtCore import QTimer
import os

class NewSongManager:
    def __init__(self, parent: object) -> None:
        self.parent = parent
        self.allow_adding = True
        self.num_displayed_widgets = 0
        self.found_song_widgets = []
        self.top_layout = None
        self.song_actions = None
        self.vertical_bar = self.parent.ui.add_songs_scroll.verticalScrollBar()
        self.vertical_bar.valueChanged.connect(self.value_changed)

        # Create a timer so it doesn't add multiple new widgets when it's supposed to do it once
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(500)
        self.timer.timeout.connect(lambda: self.reset_allow_adding())

    def value_changed(self) -> None:
        """
        Displays new songs and starts a timer to lock displaying more songs
        :return: None
        """
        if self.vertical_bar.maximum() - self.vertical_bar.value() < 500:
            if self.allow_adding:
                self.display_next_50()
                self.allow_adding = False  # Pause allowance of adding new widgets for 500ms
                self.timer.start()

    def reset_allow_adding(self) -> None:
        """
        Allow displaying new songs again
        :return: None
        """
        self.allow_adding = True
        self.value_changed()  # If already at end again, add new widgets

    def add_songs(self) -> None:
        """
        Get the songs that should be displayed
        :return: None
        """
        self.num_displayed_widgets = 0  # Reset counter
        self.top_layout = self.parent.clear_field(self.parent.ui.add_songs_scroll_content, QVBoxLayout())
        self.parent.set_page(5)
        music_dirs = self.parent.db_access.config.get_music_dirs()
        all_songs = []
        for music_dir in music_dirs:
            songs_in_dir = [music_dir + "/" + song for song in os.listdir(music_dir)]
            all_songs.extend(songs_in_dir)

        # Show loading label
        loading_label = QLabel("Loading...")
        self.top_layout.insertWidget(self.top_layout.count() - 1, loading_label)
        QApplication.processEvents()  # Needed to display now

        new_found_songs = 0
        self.found_song_widgets = []
        for i, song_path in enumerate(all_songs):
            if i % int(len(all_songs) / 100 + 1) == 0:  # Only update once per percent to avoid performance issues | +1 to avoid modulo by 0
                loading_label.setText(f"Loading... ({round(i / len(all_songs) * 100)}%)")
                QApplication.processEvents()
            if self.parent.db_access.songs.query_path(song_path):  # Do not show existing songs
                continue
            new_found_songs += 1
            self.found_song_widgets.append(FoundSong(self.parent, song_path))

        self.top_layout = self.parent.clear_field(self.parent.ui.add_songs_scroll_content, QVBoxLayout())  # Reset layout
        bottom_layout = self.parent.clear_field(self.parent.ui.add_songs_bottom_container, QVBoxLayout(), amount_left=0)
        if new_found_songs > 0:
            self.display_next_50()
            self.song_actions = SongActions(self.parent)
            bottom_layout.addWidget(self.song_actions)
        else:
            no_new_songs_label = QLabel("No new songs found")
            self.top_layout.insertWidget(self.top_layout.count() - 1, no_new_songs_label)

    def display_next_50(self) -> None:
        """
        Display the next 50 songs
        :return: None
        """
        for i in range(50):
            if self.num_displayed_widgets >= len(self.found_song_widgets):
                return
            self.top_layout.insertWidget(self.top_layout.count() - 1, self.found_song_widgets[self.num_displayed_widgets])
            self.num_displayed_widgets += 1

    def confirm_add_song(self) -> None:
        """
        Add the songs to the db
        :return: None
        """
        # Hide the songs in the layout
        for song in self.found_song_widgets:
            song.hide()
        self.song_actions.hide()
        # Show loading label
        adding_label = QLabel("Adding...")
        self.top_layout.insertWidget(self.top_layout.count() - 1, adding_label)
        QApplication.processEvents()

        for i, found_song in enumerate(self.found_song_widgets):
            if i % int(len(self.found_song_widgets) / 100 + 1) == 0:  # Only update once per percent to avoid performance issues | +1 to avoid modulo by 0
                adding_label.setText(f"Adding... ({round(i / len(self.found_song_widgets) * 100)}%)")
                QApplication.processEvents()
            found_song_data = found_song.retrieve_final_data()
            self.parent.db_access.songs.create(found_song_data[0], found_song_data[1], found_song_data[2])
        self.parent.set_page(0)
        self.parent.db_access.search.create_index_thread()
