""" Configuration file management. """
from typing import Optional
import json
import os


class Configuration:
    """ Class that holds the configuration data. """

    # Calories data file name
    CALORIES_FILE = "calories.json"
    # Recipes folder name
    RECIPES_FOLDER = "recipes"

    @staticmethod
    def _lookup_config_file():
        # TODO make an actual lookup
        # TODO use proper os-independent naming
        return ".nutrition_config"

    def __init__(self, path: Optional[str]):
        """
        Configuration class constructior.

        Available parameters:
        - application_folder
            Required. Path to the folder with the application data.
        - log_level
            Optional. Sets the log level to the one of the following:
            ['critical', 'error', 'warning', 'info', 'debug', 'none']
            Default value is 'warning'.
        """
        if path is None:
            path = self._lookup_config_file()

        with open(path) as file:
            data = json.load(file)

        self._application_folder = os.path.abspath(data["application_folder"])
        self._log_level = data.get("log_level")

        recipes_folder = os.path.join(self._application_folder, self.RECIPES_FOLDER)
        if not os.path.exists(recipes_folder):
            os.makedirs(recipes_folder)

    def calories_data_file(self):
        """ Returns the path to the calories data file. """
        return os.path.join(self._application_folder, self.CALORIES_FILE)

    def calories_data(self):
        """ Loads and returns the calories data. """
        with open(self.calories_data_file()) as file:
            return json.load(file)

    def recipes_folder(self):
        """ Returns the path to the recipes folder. """
        return os.path.join(self._application_folder, self.RECIPES_FOLDER)

    def logging_level(self):
        """ Returns the logging level. """
        return self._log_level
