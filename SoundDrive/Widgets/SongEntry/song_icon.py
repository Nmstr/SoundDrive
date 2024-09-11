from PySide6.QtGui import QPainter, QPixmap, QPainterPath
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QWidget

class SongIcon(QWidget):
    def __init__(self, parent=None, song_data = None):
        super().__init__(parent)
        self.parent = parent
        self.song_data = song_data
        self.setFixedSize(150, 150)

    def paintEvent(self, event):  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        img = self.parent.parent.parent.get_img_data(self.song_data[2])
        if not img:
            QSvgRenderer("Assets/file-music.svg").render(painter, self.rect())
        else:
            img_map = QPixmap()
            img_map.loadFromData(img)

            # Add a rounded corner
            path = QPainterPath()
            path.addRoundedRect(self.rect(), 10, 10)
            painter.setClipPath(path)

            painter.drawPixmap(self.rect(), img_map)
