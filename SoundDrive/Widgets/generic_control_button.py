from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QWidget

class GenericControlButton(QWidget):
    def __init__(self, parent=None, image_path: str = None, press_event = None):
        super().__init__(parent)
        self.press_event = press_event
        self.parent = parent
        self.setFixedSize(50, 50)

        self.icon = QPixmap(image_path)

    def paintEvent(self, event):  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(self.rect(), self.icon)

    def mousePressEvent(self, event):  # noqa: N802
        self.press_event()
