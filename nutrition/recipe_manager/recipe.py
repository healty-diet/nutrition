""" Internal representation of the recipe. """
from typing import List
import json

from .types import RecipeName, Ingredient
from .energy_value import EnergyValue


class Recipe:
    """ Class with the internal representation of the recipe. """

    def __init__(
        self,
        name: RecipeName,
        serves_amount: int,
        ingredients: List[Ingredient],
        text: str,
        energy_value_per_serving: EnergyValue,
    ):
        self.name = name
        self.serves_amount = serves_amount
        self.ingredients = ingredients
        self.text = text
        self.energy_value_per_serving = energy_value_per_serving

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

        return Recipe(
            name=recipe_dict["name"],
            serves_amount=recipe_dict["serves_amount"],
            ingredients=recipe_dict["ingredients"],
            text=recipe_dict["text"],
            energy_value_per_serving=EnergyValue.from_dict(recipe_dict["energy_value_per_serving"]),
        )
