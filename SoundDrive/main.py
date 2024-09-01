from MenuButton.menu_button import MenuButton
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import PySoundSphere
import sys


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
        self.player.load("../song.mp3")
        self.player.volume = 0.15

        # Create menu buttons
        self.add_menu_button("home")
        self.add_menu_button("library")

        # Connect buttons
        self.ui.play_btn.clicked.connect(self.play)
        self.ui.stop_btn.clicked.connect(self.stop)

    def play(self):
        self.player.play()

    def stop(self):
        self.player.stop()

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
