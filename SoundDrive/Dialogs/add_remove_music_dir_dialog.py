from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QLineEdit, QSizePolicy

class AddRemoveMusicDirDialog(QDialog):
    def __init__(self, *, dialog_type):
        super().__init__()
        if dialog_type == "add":
            self.setWindowTitle("Add Music Dir")
            self.message = "Name of the directory to be added"
        elif dialog_type == "remove":
            self.setWindowTitle("Remove Music Dir")
            self.message = "Name of the directory to be removed"
        self.setMinimumSize(400, 100)

        qbtn = (
            QDialogButtonBox.Yes | QDialogButtonBox.Cancel
        )

        self.buttonBox = QDialogButtonBox(qbtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        self.edit = QLineEdit()
        self.edit.setPlaceholderText(self.message)
        layout.addWidget(self.edit)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
