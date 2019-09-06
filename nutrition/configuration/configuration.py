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
        if path is None:
            path = self._lookup_config_file()

        with open(path) as file:
            data = json.load(file)

        self.application_folder = os.path.abspath(data["application_folder"])

        recipes_folder = os.path.join(self.application_folder, self.RECIPES_FOLDER)
        if not os.path.exists(recipes_folder):
            os.makedirs(recipes_folder)

    def calories_data_file(self):
        """ Returns the path to the calories data file. """
        return os.path.join(self.application_folder, self.CALORIES_FILE)

    def calories_data(self):
        """ Loads and returns the calories data. """
        with open(self.calories_data_file()) as file:
            return json.load(file)

    def recipes_folder(self):
        """ Returns the path to the recipes folder. """
        return os.path.join(self.application_folder, self.RECIPES_FOLDER)
