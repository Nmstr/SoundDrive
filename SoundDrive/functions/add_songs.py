from Widgets.AddSongs.song_actions import SongActions
from Widgets.AddSongs.found_song import FoundSong
from PySide6.QtWidgets import QVBoxLayout, QLabel
import os

def add_songs(parent, music_dir) -> None:
    layout = parent.clear_field(parent.ui.add_songs_scroll_content, QVBoxLayout())
    parent.set_page(5)
    all_songs = os.listdir(music_dir)
    new_found_songs = 0
    parent.found_song_widgets = []
    for song in all_songs:
        song_path = music_dir + "/" + song
        if parent.db_access.songs.query_path(song_path):  # Do not show existing songs
            continue
        new_found_songs += 1
        parent.found_song_widgets.append(FoundSong(parent, song_path))
        layout.insertWidget(layout.count() - 1, parent.found_song_widgets[-1])

    if new_found_songs > 0:
        bottom_layout = parent.clear_field(parent.ui.add_songs_bottom_container, QVBoxLayout())
        song_actions = SongActions(parent)
        bottom_layout.addWidget(song_actions)
    else:
        no_new_songs_label = QLabel("No new songs found")
        layout.insertWidget(layout.count() - 1, no_new_songs_label)