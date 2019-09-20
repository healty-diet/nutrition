""" Shopping list widget. """

from typing import Dict
import os
import math

from PySide2.QtWidgets import QPlainTextEdit

from nutrition.recipe.types import IngredientName, IngredientAmount


class ShoppingListWidget(QPlainTextEdit):
    """ Recipe content widget. """

    def __init__(self) -> None:
        super().__init__()

        self.setReadOnly(True)

        self._ingredients: Dict[IngredientName, IngredientAmount] = dict()

    @staticmethod
    def _amount_to_str(measure: str, amount: float) -> str:
        return f"{amount} ({measure})"

    def _update_shopping_list(self) -> None:
        # Update the shopping list text.
        shopping_list = ""
        for ingredient, amounts in self._ingredients.items():
            shopping_list += f"{ingredient}: "
            shopping_list += " + ".join(map(lambda x: self._amount_to_str(*x), amounts.items()))
            shopping_list += os.linesep

        self.setPlainText(shopping_list)

    def add_ingredient(self, ingredient: IngredientName, amount: IngredientAmount) -> None:
        """ Adds the provided amount of ingredient to the list. """

        if len(amount.keys()) != 1:
            raise RuntimeError(f"Attempt to add IngredientAmount with more than 1 key: {amount}")

        measure = list(amount.keys())[0]

        # Add ingredient to the stored table.
        if ingredient not in self._ingredients:
            # New ingredient.
            self._ingredients[ingredient] = amount
        elif measure in self._ingredients[ingredient]:
            # Both ingredient and measure persist.
            self._ingredients[ingredient][measure] += amount[measure]
        else:
            self._ingredients[ingredient][measure] = amount[measure]

        self._update_shopping_list()

    def remove_ingredient(self, ingredient: IngredientName, amount: IngredientAmount) -> None:
        """ Removes the provided amount of ingredient from the list. """

        if len(amount.keys()) != 1:
            raise RuntimeError(f"Attempt to add IngredientAmount with more than 1 key: {amount}")

        measure = list(amount.keys())[0]

        # Add ingredient to the stored table.
        if ingredient not in self._ingredients:
            # No such ingredient.
            return

        if measure not in self._ingredients[ingredient]:
            # No such measure.
            return

        self._ingredients[ingredient][measure] -= amount[measure]

        # Check if we have 0 of ingredient.
        if math.isclose(self._ingredients[ingredient][measure], 0.0):
            del self._ingredients[measure]

        # Check if ingredient has no measures.
        if not self._ingredients[ingredient]:
            del self._ingredients[ingredient]

        self._update_shopping_list()
