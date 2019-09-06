""" Recipe saving & loading. """
from typing import Optional, List, Dict
import os

from .recipe import Recipe


class RecipeManager:
    """ Class that is capable of work with saving&loading recipes. """

    # Path to the directory with recipes
    _path: Optional[str] = None
    # Lookup table (name of the recipe) -> (file name)
    _lookup: Dict[str, str] = dict()

    def _get_next_file_name(self) -> str:
        files_count = len([name for name in os.listdir(self._path) if os.path.isfile(name)])

        return "{}.json".format(files_count)

    @staticmethod
    def set_path(path: str):
        """ Sets the recipe folder path. """
        RecipeManager._path = path

    def save(self, recipe: Recipe):
        """ Saves the recipe. """
        file_name = self._get_next_file_name()

        with open(file_name, "w") as file:
            file.write(recipe.as_json())

        self._lookup[recipe.name] = file_name

    def load(self, recipe_name: str) -> Recipe:
        """ Loads the recipe by name. """
        file_name = self._lookup[recipe_name]

        with open(file_name, "r") as file:
            return Recipe.from_json(file.read())

    def hint(self, recipe_part: str) -> List[str]:
        """ Returns the list of hints for name. """
        raise NotImplementedError
