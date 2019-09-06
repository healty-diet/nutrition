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

    @staticmethod
    def set_path(path: str):
        """ Sets the recipe folder path. """
        if RecipeManager._path is not None:
            raise RuntimeError("Path is already set")

        RecipeManager._path = path

        RecipeManager._build_lookup()

    def save(self, recipe: Recipe):
        """ Saves the recipe. """
        file_name = self._get_next_file_name()

        with open(file_name, "w") as file:
            file.write(recipe.as_json())

        self._lookup[recipe.name] = file_name

    def load(self, recipe_name: str) -> Recipe:
        """ Loads the recipe by name. """
        file_name = self._lookup[recipe_name]

        return self._load(file_name)

    def hint(self, recipe_part: str) -> List[str]:
        """ Returns the list of hints for name. """
        raise NotImplementedError

    @staticmethod
    def _is_json(name) -> bool:
        return os.path.isfile(name) and os.path.splitext(name)[0] == ".json"

    @staticmethod
    def _json_files() -> List[str]:
        return [name for name in os.listdir(RecipeManager._path) if RecipeManager._is_json(name)]

    @staticmethod
    def _get_next_file_name() -> str:
        files_count = len(RecipeManager._json_files())

        return "{}.json".format(files_count)

    @staticmethod
    def _load(file_name) -> Recipe:
        with open(file_name, "r") as file:
            return Recipe.from_json(file.read())

    @staticmethod
    def _build_lookup():
        files = RecipeManager._json_files()

        for file_name in files:
            recipe = RecipeManager._load(file_name)
            RecipeManager._lookup[recipe.name] = file_name
