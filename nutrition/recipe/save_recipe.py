""" Module with the Recipe Text Widget. """

from typing import Optional
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton

from .recipe_name import RecipeNameWidget
from .recipe_table import RecipeTableWidget
from .recipe_text import RecipeTextWidget
from .serves_amount import ServesAmountWidget


class SaveRecipeWidget(QWidget):
    """
    Widget that is capable of saving the recipe.
    """

    def __init__(
        self,
        recipe_name: RecipeNameWidget,
        recipe_table: RecipeTableWidget,
        recipe_text: RecipeTextWidget,
        serves_amount: ServesAmountWidget,
    ):
        super().__init__()

        save_button = QPushButton("Сохранить рецепт")

        # Layout for the save block

        save_layout = QVBoxLayout()
        save_layout.addWidget(save_button)
        save_layout.addStretch()

        self.setLayout(save_layout)

        self._recipe_name = recipe_name
        self._recipe_table = recipe_table
        self._recipe_text = recipe_text
        self._serves_amount = serves_amount
