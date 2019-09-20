""" Internal representation of the recipe. """
from typing import List
import json

from .types import RecipeName, Ingredient
from .energy_value import EnergyValue


class Recipe:
    """ Class with the internal representation of the recipe. """

    def __init__(self, name: RecipeName):
        self.name = name
        self.serves_amount = 1
        self.ingredients: List[Ingredient] = []
        self.text = ""
        self.energy_value_per_serving = EnergyValue()

    def set_data(self, serves: int, ingredients: List[Ingredient], text: str, enery_value: EnergyValue) -> None:
        """ Sets the recipe data. """
        self.serves_amount = serves
        self.ingredients = ingredients
        self.text = text
        self.energy_value_per_serving = enery_value

    def ingredients_per_serving(self) -> List[Ingredient]:
        """ Returns the list of ingredients for one serving. """
        ingredients: List[Ingredient] = []

        for ingredient in self.ingredients:
            ingredient_scaled = ingredient

            name = list(ingredient_scaled.keys())[0]

            measure = list(ingredient_scaled[name].keys())[0]

            ingredient_scaled[name][measure] /= self.serves_amount

            ingredients.append(ingredient_scaled)

        return ingredients

    def as_json(self) -> str:
        """ Represents the recipe as json. """
        recipe_dict = {
            "name": self.name,
            "serves_amount": self.serves_amount,
            "ingredients": self.ingredients,
            "text": self.text,
            "energy_value_per_serving": self.energy_value_per_serving,
        }

        return json.dumps(recipe_dict, indent=2)

    @classmethod
    def from_json(cls, json_data: str) -> "Recipe":
        """ Loads the recipe from json. """
        recipe_dict = json.loads(json_data)

        recipe = cls(recipe_dict["name"])

        recipe.set_data(
            recipe_dict["serves_amount"],
            recipe_dict["ingredients"],
            recipe_dict["text"],
            EnergyValue.from_dict(recipe_dict["energy_value_per_serving"]),
        )

        return recipe
