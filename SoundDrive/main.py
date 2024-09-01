from MenuButton.menu_button import MenuButton
from SoundDriveDB import SoundDriveDB
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import PySoundSphere
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

        # Create player
        self.player = PySoundSphere.AudioPlayer("pygame")
        self.player.volume = 0.075

        # Create db
        self.db_access = SoundDriveDB()
        self.db_access.db.create_db()

        # Create menu buttons
        self.add_menu_button("home")
        self.add_menu_button("library")

        # Connect buttons
        self.ui.play_btn.clicked.connect(self.play)
        self.ui.stop_btn.clicked.connect(self.stop)
        self.ui.last_btn.clicked.connect(self.last)
        self.ui.next_btn.clicked.connect(self.next)
        self.ui.add_songs_btn.clicked.connect(self.add_songs)

    def play(self) -> None:
        self.player.play()

    def stop(self) -> None:
        self.player.pause()

    def last(self) -> None:
        self.next()

    def next(self) -> None:
        all_songs = self.db_access.songs.query()
        import random
        song = random.choice(all_songs)
        self.player.stop()
        self.player.load(song[2])
        self.player.play()

    def add_songs(self) -> None:
        all_songs = os.listdir(MUSIC_DIR)
        for song in all_songs:
            self.db_access.songs.create(song, os.path.join(MUSIC_DIR, song))

    def add_menu_button(self, button_type) -> None:
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
