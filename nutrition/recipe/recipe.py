""" Recipe module. """

from PySide2.QtWidgets import QWidget, QVBoxLayout

from .title import TitleWidget
from .serves_amount import ServesAmountWidget
from .product import ProductWidget
from .energy_value import EnergyValueWidget
from .recipe_table import RecipeTableWidget


class RecipeWidget(QWidget):
    """ Recipe widget. """

    def __init__(self, calories_data):
        super().__init__()

        title_widget = TitleWidget()
        serves_amount_widget = ServesAmountWidget()
        product_widget = ProductWidget(calories_data)
        energy_value_widget = EnergyValueWidget()
        recipe_table_widget = RecipeTableWidget()

        product_widget.set_energy_value_widget(energy_value_widget)
        product_widget.set_recipe_table_widget(recipe_table_widget)

        serves_amount_widget.set_recipe_table_widget(recipe_table_widget)

        # Layout for the whole block
        full_layout = QVBoxLayout()
        full_layout.addWidget(title_widget)
        full_layout.addWidget(serves_amount_widget)
        full_layout.addWidget(product_widget)
        full_layout.addWidget(energy_value_widget)
        full_layout.addWidget(recipe_table_widget)

        self.setLayout(full_layout)
