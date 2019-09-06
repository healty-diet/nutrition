""" Recipe module. """

from PySide2.QtWidgets import QWidget, QVBoxLayout

from .serves_amount import ServesAmountWidget
from .product import ProductWidget
from .energy_value import EnergyValueWidget
from .recipe_table import RecipeTableWidget
from .recipe_text import RecipeTextWidget
from .save_recipe import SaveRecipeWidget


class RecipeWidget(QWidget):
    """ Recipe widget. """

    def __init__(self, calories_data):
        super().__init__()

        serves_amount_widget = ServesAmountWidget()
        product_widget = ProductWidget(calories_data)
        energy_value_widget = EnergyValueWidget()
        recipe_table_widget = RecipeTableWidget()
        recipe_text_widget = RecipeTextWidget()
        save_recipe_widget = SaveRecipeWidget()

        product_widget.set_energy_value_widget(energy_value_widget)
        product_widget.set_recipe_table_widget(recipe_table_widget)

        serves_amount_widget.set_recipe_table_widget(recipe_table_widget)

        # Layout for the whole block
        full_layout = QVBoxLayout()
        full_layout.addWidget(serves_amount_widget)
        full_layout.addWidget(product_widget)
        full_layout.addWidget(energy_value_widget)
        full_layout.addWidget(recipe_table_widget)
        full_layout.addWidget(recipe_text_widget)
        full_layout.addWidget(save_recipe_widget)

        self.setLayout(full_layout)
