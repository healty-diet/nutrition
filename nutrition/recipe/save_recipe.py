""" Module with the Recipe Text Widget. """

from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide2.QtCore import Slot

from .recipe_name import RecipeNameWidget
from .recipe_table import RecipeTableWidget
from .recipe_text import RecipeTextWidget
from .serves_amount import ServesAmountWidget

from nutrition.recipe_manager import RecipeManager, Recipe


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

        self._save_button = save_button
        self._connect_slots()

    def _connect_slots(self):
        # Lint is disabled because pylint doesn't see .connect method
        # pylint: disable=no-member
        self._save_button.clicked.connect(self._save_button_clicked)

    @Slot()
    def _save_button_clicked(self, _checked):
        name = self._recipe_name.name()
        serves_amount = self._serves_amount.serves()
        recipe = self._recipe_table.get_recipe()
        recipe_text = self._recipe_text.get_text()

        recipe = Recipe(name, serves_amount, recipe, recipe_text)

        # TODO handle recipe duplicates
        RecipeManager().save(recipe)
