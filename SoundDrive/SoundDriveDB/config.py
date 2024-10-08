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
        :return: None
        """
        self.config.read(self.config_file)
        try:
            self.config.add_section("MUSIC")
            xdg_music_dir = os.getenv('XDG_MUSIC_HOME', default=os.path.expanduser('~/Music/SoundDrive'))
            self.config.set("MUSIC", "music_dirs", xdg_music_dir)
            self.config.set("MUSIC", "initial_volume", "0.1")
            with open(self.config_file, "w") as f:
                self.config.write(f)
        except configparser.DuplicateSectionError:
            pass

    def get_music_dirs(self) -> list[str]:
        """
        Get the music directories
        :return: List of the dirs
        """
        self.config.read(self.config_file)
        try:
            value = self.config.get("MUSIC", "music_dirs")
            return value.split(",")
        except configparser.NoOptionError:
            raise f"Did not find 'music_dirs' in section 'MUSIC' of file '{self.config_file}'"

    def add_music_dir(self, music_dir: str) -> None:
        """
        Add a music dir
        :param music_dir: The dir to be added
        :return: None
        """
        if not os.path.exists(music_dir):  # Create the dir if it doesn't exist
            os.makedirs(music_dir, exist_ok=True)

        # Modify the current music dirs
        values = [music_dir for music_dir in self.get_music_dirs() if music_dir]  # Remove empty strings
        values.append(music_dir)

        # Write the new dirs
        self.config.set("MUSIC", "music_dirs", ",".join(values))
        with open(self.config_file, "w") as f:
            self.config.write(f)

    def remove_music_dir(self, music_dir: str) -> None:
        """
        Remove a music dir
        :param music_dir: The dir to be removed
        :return: None
        """
        # Modify the current music dirs
        values = self.get_music_dirs()
        values.remove(music_dir)

        # Write the new values
        self.config.set("MUSIC", "music_dirs", ",".join(values))
        with open(self.config_file, "w") as f:
            self.config.write(f)

    @property
    def initial_volume(self) -> float:
        """
        The initial volume when the application starts
        """
        self.config.read(self.config_file)
        try:
            value = self.config.get("MUSIC", "initial_volume")
            return float(value)
        except configparser.NoOptionError:
            return 0.1

    @initial_volume.setter
    def initial_volume(self, initial_volume: float) -> None:
        self.config.set("MUSIC", "initial_volume", str(initial_volume))
        with open(self.config_file, "w") as f:
            self.config.write(f)
