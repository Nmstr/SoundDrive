from Widgets.AddSongs.song_actions import SongActions
from Widgets.AddSongs.found_song import FoundSong
from PySide6.QtWidgets import QVBoxLayout, QLabel, QApplication
from PySide6.QtCore import QTimer
import os

class NewSongManager:
    def __init__(self, parent):
        self.parent = parent
        self.allow_adding = True
        self.num_displayed_widgets = 0
        self.found_song_widgets = []
        self.top_layout = None
        self.vertical_bar = self.parent.ui.add_songs_scroll.verticalScrollBar()
        self.vertical_bar.valueChanged.connect(self.value_changed)

        # Create a timer so it doesn't add multiple new widgets when it's supposed to do it once
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(500)
        self.timer.timeout.connect(lambda: self.reset_allow_adding())

    def value_changed(self):
        if self.vertical_bar.maximum() - self.vertical_bar.value() < 500:
            if self.allow_adding:
                self.display_next_50()
                self.allow_adding = False  # Pause allowance of adding new widgets for 500ms
                self.timer.start()

    def reset_allow_adding(self):
        self.allow_adding = True
        self.value_changed()  # If already at end again, add new widgets

    def add_songs(self, music_dir) -> None:
        self.top_layout = self.parent.clear_field(self.parent.ui.add_songs_scroll_content, QVBoxLayout())
        self.parent.set_page(5)
        all_songs = os.listdir(music_dir)

        # Show loading label
        loading_label = QLabel("Loading...")
        self.top_layout.insertWidget(self.top_layout.count() - 1, loading_label)
        QApplication.processEvents()  # Needed to display now

        new_found_songs = 0
        self.found_song_widgets = []
        for i, song in enumerate(all_songs):
            loading_label.setText(f"Loading... ({i}/{len(all_songs)})")
            if i % 100 == 0:  # Only update once every 100 avoid performance issues
                QApplication.processEvents()
            song_path = music_dir + "/" + song
            if self.parent.db_access.songs.query_path(song_path):  # Do not show existing songs
                continue
            new_found_songs += 1
            self.found_song_widgets.append(FoundSong(self.parent, song_path))

        self.top_layout = self.parent.clear_field(self.parent.ui.add_songs_scroll_content, QVBoxLayout())  # Reset layout
        if new_found_songs > 0:
            self.display_next_50()
            bottom_layout = self.parent.clear_field(self.parent.ui.add_songs_bottom_container, QVBoxLayout())
            song_actions = SongActions(self.parent)
            bottom_layout.addWidget(song_actions)
        else:
            no_new_songs_label = QLabel("No new songs found")
            self.top_layout.insertWidget(self.top_layout.count() - 1, no_new_songs_label)

    def display_next_50(self):
        for i in range(50):
            self.top_layout.insertWidget(self.top_layout.count() - 1, self.found_song_widgets[self.num_displayed_widgets])
            self.num_displayed_widgets += 1

    def confirm_add_song(self):
        for found_song in self.found_song_widgets:
            found_song_data = found_song.retrieve_final_data()
            self.parent.db_access.songs.create(found_song_data[0], found_song_data[1], found_song_data[2])
        self.parent.set_page(0)
        self.parent.db_access.search.create_index_thread()
