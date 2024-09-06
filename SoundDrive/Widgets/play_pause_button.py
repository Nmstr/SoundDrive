from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QWidget

class PlayPauseButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.is_playing = False
        self.setFixedSize(50, 50)

        self.play_icon = QPixmap("Assets/play.svg")
        self.pause_icon = QPixmap("Assets/pause.svg")

    def paintEvent(self, event):  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the icon
        if self.parent.music_controller.is_playing:
            painter.drawPixmap(self.rect(), self.pause_icon)
        else:
            painter.drawPixmap(self.rect(), self.play_icon)

    def mousePressEvent(self, event):  # noqa: N802
        if self.parent.music_controller.is_playing:
            self.parent.music_controller.stop()
        else:
            self.parent.music_controller.continue_playback()
        self.update()
