""" Internal representation of the recipe. """
from typing import Dict
import json


class Recipe:
    """ Class with the internal representation of the recipe. """

    def __init__(self, name: str, serves_amount: int, ingredients: Dict[str, Dict[str, float]], text: str):
        self.name = name
        self.serves_amount = serves_amount
        self.ingredients = ingredients
        self.text = text

    def as_json(self) -> str:
        """ Represents the recipe as json. """
        recipe_dict = {
            "name": self.name,
            "serves_amount": self.serves_amount,
            "ingredients": self.ingredients,
            "text": self.text,
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
        )
