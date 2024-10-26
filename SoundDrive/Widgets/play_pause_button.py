from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QWidget

class PlayPauseButton(QWidget):
    def __init__(self, parent: object = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.is_playing = False
        self.setFixedSize(50, 50)

        self.play_icon = QPixmap("Assets/play.svg")
        self.pause_icon = QPixmap("Assets/pause.svg")

    def paintEvent(self, event) -> None:  # noqa: N802
        """
        Paint the icon
        :return: None
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the icon
        if self.parent.music_controller.is_playing:
            painter.drawPixmap(self.rect(), self.pause_icon)
        else:
            painter.drawPixmap(self.rect(), self.play_icon)

    def mousePressEvent(self, event):  # noqa: N802
        if self.parent.music_controller.is_playing:
            self.parent.music_controller.pause()
        else:
            self.parent.music_controller.unpause()
        self.update()
