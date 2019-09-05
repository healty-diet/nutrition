from typing import Optional, Dict, Union
import logging
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QCompleter, QPushButton, QHBoxLayout
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QIntValidator

from .utils import energy_data_str, scale
from .energy_value import EnergyValueWidget
from .recipe_table import RecipeTableWidget


class ProductWidget(QWidget):
    def __init__(self, calories_data: Dict[str, Union[str, float]]):
        super().__init__()

        self.calories_data = calories_data
        self.calories_word_list = list(self.calories_data.keys())

        self.energy_value_widget: Optional[EnergyValueWidget] = None
        self.recipe_table_widget: Optional[RecipeTableWidget] = None

        # Product
        product_label = QLabel("Продукт:")
        product_line_edit = QLineEdit()

        # Completer for the product line edit
        completer = QCompleter(self.calories_word_list)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        product_line_edit.setCompleter(completer)

        # Product mass line edit
        product_mass_line_edit = QLineEdit()
        product_mass_line_edit.setPlaceholderText("Масса (гр.)")
        product_mass_line_edit.setFixedWidth(100)
        product_mass_line_edit.setValidator(QIntValidator())
        product_mass_line_edit.setMaxLength(4)

        # Button to add product to the recipe

        product_add_button = QPushButton("+")

        # Layout for product_label / product_line_edit
        product_layout = QHBoxLayout()
        product_layout.addWidget(product_label)
        product_layout.addWidget(product_line_edit)
        product_layout.addWidget(product_mass_line_edit)
        product_layout.addWidget(product_add_button)

        self.setLayout(product_layout)

        self.product_line_edit = product_line_edit
        self.product_mass_line_edit = product_mass_line_edit
        self.product_add_button = product_add_button

    def set_energy_value_widget(self, energy_value_widget: EnergyValueWidget):
        """ Sets field to interact with energy data module """
        self.energy_value_widget = energy_value_widget
        self._connect_energy_data_slots()

    def set_recipe_table_widget(self, recipe_table_widget: RecipeTableWidget):
        """ Sets field to interact with recipe table module """
        self.recipe_table_widget = recipe_table_widget

        self._connect_recipe_data_slots()

    def _connect_energy_data_slots(self):
        """ Connects slots associated with energy data. """
        # Lint is disabled because pylint doesn't see .connect method
        # pylint: disable=no-member

        # Slot to be called when product name was entered.
        self.product_line_edit.editingFinished.connect(self._product_name_was_entered)

        # Slot to be called when product mass was entered.
        self.product_mass_line_edit.editingFinished.connect(self._product_mass_was_entered)

    def _connect_recipe_data_slots(self):
        """ Connects slots associated with recipe data. """
        # Lint is disabled because pylint doesn't see .connect method
        # pylint: disable=no-member

        # Slot to be called when product add button was clicked.
        self.product_add_button.clicked.connect(self._add_product_to_recipe)

    @Slot()
    def _product_name_was_entered(self):
        """ Slot for the product search. """
        product = self.product_line_edit.text()

        product_data = self.calories_data.get(product)
        if product_data:
            logging.debug("Completed product lookup: %s", product)

            energy_data = energy_data_str(product_data)

            self.energy_value_widget.set_text(energy_data)

    @Slot()
    def _product_mass_was_entered(self):
        """ Slot to calculate energy values for entered mass. """

        product = self.product_line_edit.text()
        product_mass = self.product_mass_line_edit.text()

        product_data = self.calories_data.get(product)
        if not product_data or not product_mass.isdigit():
            # Incorrect data, do nothing
            return

        logging.debug("Completed product lookup with mass: %s / %s", product, product_mass)

        energy_data = energy_data_str(product_data, product_mass, needs_scaling=True)

        self.energy_value_widget.set_text(energy_data)

    @Slot()
    def _add_product_to_recipe(self):
        """ Slot for adding product to the recipe. """
        product = self.product_line_edit.text()
        product_mass = self.product_mass_line_edit.text()

        product_data = self.calories_data.get(product)
        if not product_data or not product_mass.isdigit():
            # Incorrect data, do nothing.
            return

        energy_data = list(
            scale(
                [product_data["calories"], product_data["protein"], product_data["fat"], product_data["carbohydrates"]],
                scale_factor=product_mass,
            )
        )

        recipe_element = {
            "name": product,
            "mass": product_mass,
            "calories": energy_data[0],
            "protein": energy_data[1],
            "fat": energy_data[2],
            "carbohydrates": energy_data[3],
        }

        self.recipe_table_widget.add_recipe_element(recipe_element)
