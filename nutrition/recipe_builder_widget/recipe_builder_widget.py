""" Recipe module. """

from PySide2.QtWidgets import QWidget, QVBoxLayout

from nutrition.logger import Logger
from nutrition.recipe.types import Ingredient, IngredientName, IngredientAmount, MeasureName
from nutrition.recipe import RecipeManager

from .widgets.recipe_name import RecipeNameWidget
from .widgets.serves_amount import ServesAmountWidget
from .widgets.ingredient import IngredientWidget
from .widgets.energy_value import EnergyValueWidget
from .widgets.recipe_table import RecipeTableWidget
from .widgets.recipe_text import RecipeTextWidget
from .widgets.save_recipe import SaveRecipeWidget
from .widgets.total_energy_value import TotalEnergyValueWidget
from .widgets.utils import scale
from .recipe_builder import RecipeBuilder


class RecipeBuilderWidget(QWidget):
    """ Recipe widget. """

    def __init__(self, calories_data):
        super().__init__()

        self._calories_data = calories_data

        food_names_list = list(self._calories_data.keys())

        self._serves = 1
        self._recipe_builder = RecipeBuilder()

        self._recipe_name_widget = RecipeNameWidget()
        self._serves_amount_widget = ServesAmountWidget(self._serves_amount_edited)
        self._product_widget = IngredientWidget(food_names_list, self._ingredient_entered, self._ingredient_finalized)
        self._energy_value_widget = EnergyValueWidget()
        self._recipe_table_widget = RecipeTableWidget()
        self._total_energy_value_widget = TotalEnergyValueWidget()
        self._recipe_text_widget = RecipeTextWidget()
        self._save_recipe_widget = SaveRecipeWidget(self._on_save_button_clicked)

        # Layout for the whole block
        full_layout = QVBoxLayout()
        full_layout.addWidget(self._recipe_name_widget)
        full_layout.addWidget(self._serves_amount_widget)
        full_layout.addWidget(self._product_widget)
        full_layout.addWidget(self._energy_value_widget)
        full_layout.addWidget(self._recipe_table_widget)
        full_layout.addWidget(self._total_energy_value_widget)
        full_layout.addWidget(self._recipe_text_widget)
        full_layout.addWidget(self._save_recipe_widget)

        self.setLayout(full_layout)

    def _ingredient_entered(self, ingredient_name: str, ingredient_mass: float):
        # Callback that is called when ingredient data is entered.

        ingredient_data = self._calories_data.get(ingredient_name)
        if not ingredient_data:
            # Incomplete data, do nothing
            return

        Logger.get_logger().debug("Completed ingredient lookup with mass: %s / %s", ingredient_name, ingredient_mass)

        # Update product energy value.
        self._energy_value_widget.set_energy_value(ingredient_data, ingredient_mass)

    def _ingredient_finalized(self, ingredient_name: str, ingredient_mass: float):
        # Callback that is called when ingredient data is finalized (ready to be added to the recipe).

        ingredient_data = self._calories_data.get(ingredient_name)
        if not ingredient_data:
            # Incomplete data, do nothing
            return

        # Sacle ingredient energy data to the mass.
        ingredient_data = scale(ingredient_data, ingredient_mass)

        Logger.get_logger().debug("Adding ingredient to the recipe: %s", ingredient_name)

        # Create an ingredient.
        ingredient = Ingredient(
            {IngredientName(ingredient_name): IngredientAmount({MeasureName("гр."): ingredient_mass})}
        )

        # Add the ingredient to the recipe table.
        self._recipe_table_widget.add_ingredient(ingredient_name, ingredient_data, ingredient_mass)

        # Add the ingredient to the recipe builder.
        self._recipe_builder.add_ingredient(ingredient, ingredient_data)

        # Set the total recipe energy value.
        self._total_energy_value_widget.set_total(self._recipe_builder.energy_value())

    def _serves_amount_edited(self, new_amount: int):
        # Callback that is called when serves amount is entered.

        self._serves = new_amount

        # Update the recipe builder and total energy value.
        self._recipe_builder.set_serves(self._serves)
        self._total_energy_value_widget.set_total(self._recipe_builder.energy_value())

    def _recipe_element_removed(self, recipe_element):
        raise NotImplementedError

    def _on_save_button_clicked(self):
        # Callback that is called when recipe is ready and should be saved.

        # Update final recipe builder data.
        self._recipe_builder.set_recipe_name(self._recipe_name_widget.name())
        self._recipe_builder.set_recipe_text(self._recipe_text_widget.get_text())

        # TODO handle recipe duplicates
        try:
            RecipeManager().save(self._recipe_builder.build())
        except RuntimeError:
            Logger.get_logger().warning("Save button clicked with incomplete recipe")
