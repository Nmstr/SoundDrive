from Dialogs.edit_playlist_dialog import EditPlaylistDialog

def create_playlist(parent) -> None:
    """
    Creates a playlist and updates the UI.
    :return: None
    """
    parent.db_access.playlists.create()
    parent.populate_playlists()


def delete_playlist(parent) -> None:
    """
    Deletes the selected playlist and updates the UI.
    Opens a dialog for confirmation
    :return: None
    """
    dlg = EditPlaylistDialog(parent.db_access, parent.current_playlist, dialog_type="delete")
    if dlg.exec():
        parent.db_access.playlists.delete(parent.current_playlist)

    parent.set_page(0)
    parent.populate_playlists()


def rename_playlist(parent) -> None:
    """
    Rename a playlist
    :return: None
    """
    dlg = EditPlaylistDialog(parent.db_access, parent.current_playlist, dialog_type="rename")
    if dlg.exec():
        parent.db_access.playlists.rename(parent.current_playlist, dlg.edit.text())

    parent.populate_playlists()
    parent.playlist_dict[parent.current_playlist].activate()
