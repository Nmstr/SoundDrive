from PySide6.QtWidgets import QFrame
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QFile

class MenuButton(QFrame):
    def __init__(self, parent = None, type = None) -> None:
        super().__init__(parent)
        self.parent = parent
        if type == "home":
            self.label_text = "Home"
            self.destination = 0
        elif type == "library":
            self.label_text = "Library"
            self.destination = 1
        else:
            raise ValueError

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("MenuButton/menu_button.ui")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.ui.button_label.setText(self.label_text)

    def mousePressEvent(self, event):  # noqa: N802
        if event.button() == Qt.LeftButton:
            self.parent.set_page(self.destination)
        return super().mousePressEvent(event)
