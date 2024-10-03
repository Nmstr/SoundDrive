from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt

class VolumeSlider(QSlider):
    def __init__(self, parent: object = None, initial_volume: int = 0.075) -> None:
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.parent = parent
        self.setRange(0, 1000)
        self.setValue(initial_volume * 1000)
        self.valueChanged.connect(self.value_changed)

    def mousePressEvent(self, event):  # noqa: N802
        """
        Change the position of the slider
        """
        if event.button() == Qt.LeftButton:
            value = self.minimum() + (self.maximum() - self.minimum()) * event.position().x() / self.width()
            self.setValue(int(value))
        super().mousePressEvent(event)

    def value_changed(self) -> None:
        """
        Changed the volume
        :return: None
        """
        self.parent.music_controller.volume = self.value() / 1000 / 2  # The 2 halves from max volume to prevent ear damage and improves precision when setting reasonable values
        print(int(self.value() / 10))
        self.parent.ui.volume_label.setText(f"{round(self.value() / 10)}%")
