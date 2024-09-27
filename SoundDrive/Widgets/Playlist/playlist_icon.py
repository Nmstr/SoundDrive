from Functions.covers import get_playlist_icon
from PySide6.QtGui import QPainter, QPixmap, QPainterPath
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QWidget

class PlaylistIcon(QWidget):
    def __init__(self, parent: object = None,
                 playlist_data: list[str] = None,
                 *, size: tuple = (150, 150)) -> None:
        super().__init__(parent)
        self.parent = parent
        self.playlist_data = playlist_data
        self.wanted_width, self.wanted_height = size
        self.setFixedSize(self.wanted_width, self.wanted_height)

    def paintEvent(self, event) -> None:  # noqa: N802
        """
        Paint the song icon
        :return: None
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.playlist_data[3]:
            img = get_playlist_icon(self.playlist_data,
                                     resolution = (self.wanted_width, self.wanted_height),
                                     db_access = self.parent.parent.db_access)
        else:
            img = None
        if not img:
            QSvgRenderer("Assets/playlist.svg").render(painter, self.rect())
        else:
            img_map = QPixmap()
            img_map.loadFromData(img)

            # Add a rounded corner
            path = QPainterPath()
            path.addRoundedRect(self.rect(), 10, 10)
            painter.setClipPath(path)

            painter.drawPixmap(self.rect(), img_map)
