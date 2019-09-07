""" Recipe saving & loading. """
from typing import Optional, List, Dict
import os

from nutrition.logger import Logger
from .recipe import Recipe


class RecipeManager:
    """ Class that is capable of work with saving&loading recipes. """

    # Path to the directory with recipes
    _path: Optional[str] = None
    # Lookup table (name of the recipe) -> (file name)
    _lookup: Dict[str, str] = dict()

    @classmethod
    def set_path(cls, path: str):
        """ Sets the recipe folder path. """
        if cls._path is not None:
            raise RuntimeError("Path is already set")

        cls._path = path

        cls._build_lookup()

    @classmethod
    def path(cls) -> str:
        """ Returns the stored path. """
        if cls._path is None:
            raise RuntimeError("Path for RecipeManager is not set")
        return cls._path

    def save(self, recipe: Recipe):
        """ Saves the recipe. """
        # TODO handle recipe duplicates (by name)

        file_name = self._get_next_file_name()
        file_path = os.path.join(self.path(), file_name)

        Logger.get_logger().debug("Saving recipe '{}' to file {}".format(recipe.name, file_path))

        with open(file_path, "w") as file:
            file.write(recipe.as_json())

        self._lookup[recipe.name] = file_name

    def load(self, recipe_name: str) -> Recipe:
        """ Loads the recipe by name. """

        Logger.get_logger().debug("Loading recipe '{}'".format(recipe_name))

        file_name = self._lookup[recipe_name]

        return self._load(file_name)

    def hint(self, recipe_part: str) -> List[str]:
        """ Returns the list of hints for name. """

        raise NotImplementedError

    @staticmethod
    def _is_json(name) -> bool:
        return os.path.splitext(name)[1] == ".json"

    @classmethod
    def _json_files(cls) -> List[str]:
        return [name for name in os.listdir(cls.path()) if cls._is_json(name)]

    @classmethod
    def _get_next_file_name(cls) -> str:
        print([name for name in os.listdir(cls.path()) if cls._is_json(name)])
        files_count = len(cls._json_files())

        return "{}.json".format(files_count)

    @classmethod
    def _load(cls, file_name) -> Recipe:
        file_path = os.path.join(cls.path(), file_name)
        with open(file_path, "r") as file:
            return Recipe.from_json(file.read())

    @classmethod
    def _build_lookup(cls):
        files = cls._json_files()

        for file_name in files:
            recipe = cls._load(file_name)
            cls._lookup[recipe.name] = file_name
