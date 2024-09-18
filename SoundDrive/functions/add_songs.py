from Widgets.AddSongs.song_actions import SongActions
from Widgets.AddSongs.found_song import FoundSong
from PySide6.QtWidgets import QVBoxLayout, QLabel
import os

class NewSongManager:
    def __init__(self, parent):
        self.parent = parent

    def add_songs(self, music_dir) -> None:
        layout = self.parent.clear_field(self.parent.ui.add_songs_scroll_content, QVBoxLayout())
        self.parent.set_page(5)
        all_songs = os.listdir(music_dir)
        new_found_songs = 0
        self.parent.found_song_widgets = []
        for song in all_songs:
            song_path = music_dir + "/" + song
            if self.parent.db_access.songs.query_path(song_path):  # Do not show existing songs
                continue
            new_found_songs += 1
            print(new_found_songs)
            self.parent.found_song_widgets.append(FoundSong(self.parent, song_path))
            layout.insertWidget(layout.count() - 1, self.parent.found_song_widgets[-1])

        if new_found_songs > 0:
            bottom_layout = self.parent.clear_field(self.parent.ui.add_songs_bottom_container, QVBoxLayout())
            song_actions = SongActions(self.parent)
            bottom_layout.addWidget(song_actions)
        else:
            no_new_songs_label = QLabel("No new songs found")
            layout.insertWidget(layout.count() - 1, no_new_songs_label)

    def confirm_add_song(self):
        for found_song in self.parent.found_song_widgets:
            found_song_data = found_song.retrieve_final_data()
            self.parent.db_access.songs.create(found_song_data[0], found_song_data[1], found_song_data[2])
        self.parent.set_page(0)
        self.parent.db_access.search.create_index_thread()
