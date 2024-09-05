from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout

class DeletePlaylistDialog(QDialog):
    def __init__(self, db_access, current_playlist):
        super().__init__()
        self.setWindowTitle("Delete Playlist")
        playlist_data = db_access.playlists.query_id(current_playlist)

        qbtn = (
            QDialogButtonBox.Yes | QDialogButtonBox.Cancel
        )

        self.buttonBox = QDialogButtonBox(qbtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel(f"Do you really want to delete \"{playlist_data[1]}\"? (ID: {playlist_data[0]})")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
