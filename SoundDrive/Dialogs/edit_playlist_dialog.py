from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QLineEdit

class EditPlaylistDialog(QDialog):
    def __init__(self, db_access: object, current_playlist: int, dialog_type: str) -> None:
        super().__init__()
        playlist_data = db_access.playlists.query_id(current_playlist)
        layout = QVBoxLayout()
        if dialog_type == "delete":
            self.setWindowTitle("Delete Playlist")
            message = QLabel(f"Do you really want to delete \"{playlist_data[1]}\"? (ID: {playlist_data[0]})")
            layout.addWidget(message)
        elif dialog_type == "rename":
            self.setWindowTitle("Rename Playlist")
            self.edit = QLineEdit()
            self.edit.setPlaceholderText("New name of the playlist")
            layout.addWidget(self.edit)
        self.setMaximumSize(400, 100)

        qbtn = (
            QDialogButtonBox.Yes | QDialogButtonBox.Cancel
        )

        self.buttonBox = QDialogButtonBox(qbtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
