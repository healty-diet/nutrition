""" Recipe builder. """

from typing import Optional, List
from functools import wraps

from nutrition.recipe.types import RecipeName, Ingredient
from nutrition.recipe import Recipe
from nutrition.recipe.energy_value import EnergyValue


def _affects_recipe(method):
    """ Methods marked with this decorator will recalculate the recipe after the method call. """

    @wraps(method)
    def wrapper(self: "RecipeBuilder", *args):
        result = method(self, *args)
        self.recalculate()
        return result

    return wrapper


class RecipeBuilder:
    """ Class that builds recipe. """

    def __init__(self):
        self._recipe_name: Optional[RecipeName] = None
        self._ingredients: List[(Ingredient, EnergyValue)] = []
        self._text: Optional[str] = None
        self._energy_value_per_serving: EnergyValue = EnergyValue()
        self._serves = 1

    def energy_value(self):
        """ Getter for the recipe energy value. """
        return self._energy_value_per_serving

    def set_recipe_name(self, recipe_name: RecipeName):
        """ Sets recipe name. """
        self._recipe_name = recipe_name

    def set_recipe_text(self, recipe_text: str):
        """ Sets the recipe text. """
        self._text = recipe_text

    @_affects_recipe
    def set_serves(self, serves: int):
        """ Sets the amount of service in the recipe. """
        self._serves = serves

    @_affects_recipe
    def add_ingredient(self, ingredient: Ingredient, energy_value: EnergyValue):
        """ Adds an ingredient to the recipe. """
        self._ingredients.append((ingredient, energy_value))

    @_affects_recipe
    def remove_ingredient(self, ingredient: Ingredient):
        """ Removes an ingredient from the recipe. """
        raise NotImplementedError

    def build(self) -> Recipe:
        """ Builds a Recipe object from the stored data. """
        if self._recipe_name is None or not self._ingredients or self._text is None:
            raise RuntimeError("Attempt to build incomplete recipe")

        ingredients_list = list(map(lambda el: el[0], self._ingredients))
        recipe = Recipe(self._recipe_name, self._serves, ingredients_list, self._text, self._energy_value_per_serving)

        return recipe

    def recalculate(self):
        """ Recalculates the recipe values. """
        self._energy_value_per_serving = EnergyValue()

        for ingredient in self._ingredients:
            for key in ingredient[1]:
                self._energy_value_per_serving[key] += ingredient[1][key]

        for key in self._energy_value_per_serving:
            self._energy_value_per_serving[key] /= self._serves
