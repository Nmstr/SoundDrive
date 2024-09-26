from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt, QTimer

class TimeSlider(QSlider):
    def __init__(self, parent: object = None) -> None:
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.parent = parent
        self.setRange(0, 1000)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_value)
        self.timer.start(250)

    def mousePressEvent(self, event):  # noqa: N802
        """
        Set the song position
        """
        if event.button() == Qt.LeftButton:
            value = self.minimum() + (self.maximum() - self.minimum()) * event.position().x() / self.width()
            self.setValue(int(value))
            song_length = self.parent.music_controller.song_length
            self.parent.music_controller.song_position = value / 1000 * song_length
        super().mousePressEvent(event)

    def update_value(self) -> None:
        """
        Update the slider position
        """
        song_position = self.parent.music_controller.song_position
        song_length = self.parent.music_controller.song_length
        if song_length == 0:
            return
        self.setValue(song_position / song_length * 1000)
        self.parent.update_song_times(song_position)
