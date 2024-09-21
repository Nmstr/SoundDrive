import configparser
import os

class Config:
    def __init__(self) -> None:
        config_path = os.getenv('XDG_CONFIG_HOME', default=os.path.expanduser('~/.config')) + '/SoundDrive/'
        if not os.path.exists(config_path):
            os.makedirs(config_path, exist_ok=True)
        self.config_file = config_path + 'config.ini'
        self.config = configparser.ConfigParser()
        self._create_config_file()

    def _create_config_file(self) -> None:
        """
        Create the config file
        """
        self.config.read(self.config_file)
        try:
            self.config.add_section("MUSIC")
            xdg_music_dir = os.getenv('XDG_MUSIC_HOME', default=os.path.expanduser('~/Music/SoundDrive'))
            self.config.set("MUSIC", "music_dirs", xdg_music_dir)
            with open(self.config_file, "w") as f:
                self.config.write(f)
        except configparser.DuplicateSectionError:
            pass

    def add_music_dir(self, music_dir: str) -> None:
        if not os.path.exists(music_dir):  # Create the dir if it doesn't exist
            os.makedirs(music_dir, exist_ok=True)

        # Retrieve existing values
        self.config.read(self.config_file)
        try:
            value = self.config.get("MUSIC", "music_dirs")
        except configparser.NoOptionError:
            raise f"Did not find 'music_dirs' in section 'MUSIC' of file '{self.config_file}'"

        # Append new dir
        values = value.split(',')
        values.append(music_dir)

        # Write the new values
        self.config.set("MUSIC", "music_dirs", ",".join(values))
        with open(self.config_file, "w") as f:
            self.config.write(f)

    def remove_music_dir(self, music_dir: str) -> None:
        # Retrieve existing values
        self.config.read(self.config_file)
        try:
            value = self.config.get("MUSIC", "music_dirs")
        except configparser.NoOptionError:
            raise f"Did not find 'music_dirs' in section 'MUSIC' of file '{self.config_file}'"

        # Remove the dir
        values = value.split(',')
        values.remove(music_dir)

        # Write the new values
        self.config.set("MUSIC", "music_dirs", ",".join(values))
        with open(self.config_file, "w") as f:
            self.config.write(f)
