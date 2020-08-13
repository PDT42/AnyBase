"""
:Auth: PDT
:Since: 2020/05/24

This is the config module, it contains the Config class. The Config contains all values that must be set before
launching the application.
"""

import os

from configparser import ConfigParser


class Config:
    """This is an adapter to access a config.ini file."""

    _instance = None
    _path = "res/config.ini"

    @staticmethod
    def get() -> 'Config':
        """Get the instance of this singleton."""

        if not Config._instance:
            Config._instance = Config()
        return Config._instance

    def read(self, section, key, default=None):
        """Read a key from the config."""

        config = ConfigParser()
        config.read(self._path)

        if default and section not in config:
            config[section] = {}

        if section not in config.sections():
            raise ValueError("You specified an unknown section of the config!")

        if key not in config[section]:
            config[section][key] = default
        res = config[section][key]

        with open(self._path, 'w') as configfile:
            config.write(configfile)
        return res

    def insert(self, section, key, value):
        """Insert a key into the config."""

        config = ConfigParser()
        config.read(self._path)

        if section not in config:
            config[section] = {}

        config[section][key] = value

        with open(self._path, 'w') as configfile:
            config.write(configfile)

    def change_path(self, path):
        """Change where this looks for the .ini."""

        if not os.path.exists(path):
            raise ValueError("The specified path does not exist!")

        self._path = path
