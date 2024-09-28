from Dialogs.add_remove_music_dir_dialog import AddRemoveMusicDirDialog

def add_music_dir(parent) -> None:
    """
    Adds a music dir to the config and updates the UI
    :return: None
    """
    dlg = AddRemoveMusicDirDialog(dialog_type="add")
    if dlg.exec():
        parent.db_access.config.add_music_dir(dlg.edit.text())
        parent.populate_settings_music_dir()


def remove_music_dir(parent) -> None:
    """
    Removes a music dir from the config and updates the UI
    :return: None
    """
    dlg = AddRemoveMusicDirDialog(dialog_type="remove")
    if dlg.exec():
        parent.db_access.config.remove_music_dir(dlg.edit.text())
        parent.populate_settings_music_dir()
