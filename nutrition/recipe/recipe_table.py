""" Module with the Recipe Table Widget. """

from typing import Dict, List
from enum import Enum
from PySide2.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem

from nutrition.utils import InfoWithLabel
from .utils import energy_data_str


def _table_item(value):
    """ Returns QTableWidgetItem with the string as value. """

    return QTableWidgetItem(str(value))


class RecipeTableWidget(QWidget):
    """
    Widget that is capable of handling the recipe itself.
    It contains the table with the ingredients and the field with total recipe energy value.
    """

    class TableColumns(Enum):
        """ Enum for describing table columns. """

        # Lint is disabled because pylint doesn't recognize Enum's .value attribute
        # pylint: disable=invalid-sequence-index

        PRODUCT = 0
        MASS = 1
        CALORIES = 2
        PROTEIN = 3
        FAT = 4
        CARBOHYDRATES = 5

        def __str__(self) -> str:
            names = ["name", "mass", "calories", "protein", "fat", "carbohydrates"]

            return names[self.value]

        def translated_str(self) -> str:
            """ Works as __str__ but returns a translated string. """

            names = ["Продукт", "Масса", "К", "Б", "Ж", "У"]

            return names[self.value]

        @classmethod
        def product_data_indices(cls) -> List["RecipeTable.TableColumns"]:
            """ Returns indices for product data fields. """
            return [cls(idx) for idx in range(cls.MASS.value, cls.CARBOHYDRATES.value + 1)]

    def __init__(self):
        super().__init__()

        columns = [el.translated_str() for el in self.TableColumns]
        recipe_contents = QTableWidget(0, len(columns))
        recipe_contents.setHorizontalHeaderLabels(columns)
        recipe_contents.setFixedWidth(700)
        recipe_contents.horizontalHeader().setDefaultSectionSize(50)
        recipe_contents.setColumnWidth(0, 350)

        recipe_total_widget = InfoWithLabel("Итого:", width=300)

        recipe_total_per_unit_widget = InfoWithLabel("Итого (на порцию):", width=300)

        # Layout for the recipe block

        recipe_layout = QVBoxLayout()
        recipe_layout.addWidget(recipe_contents)
        recipe_layout.addWidget(recipe_total_widget)
        recipe_layout.addWidget(recipe_total_per_unit_widget)

        self.setLayout(recipe_layout)

        self.recipe_contents = recipe_contents
        self.recipe_total = recipe_total_widget
        self.recipe_total_per_unit = recipe_total_per_unit_widget
        self.serves_amount = 1  # 1 by default

    def set_serves_amount(self, serves_amount: int):
        """ Sets the serves amount. """
        self.serves_amount = serves_amount

    def set_recipe_total_info(self, total: Dict[str, float]):
        """ Sets the total info about the recipe to the text label. """

        energy_data = energy_data_str(total, total["mass"])
        self.recipe_total.set_text(energy_data)

        for key in total:
            total[key] /= self.serves_amount

        energy_data_per_unit = energy_data_str(total, total["mass"])
        self.recipe_total_per_unit.set_text(energy_data_per_unit)

    def add_recipe_element(self, element_name: str, element: Dict[str, float]):
        """ Adds a new row into recipe table with provided ingredient. """

        row_count = self.recipe_contents.rowCount()
        self.recipe_contents.insertRow(row_count)

        # Set name
        self.recipe_contents.setItem(row_count, self.TableColumns.PRODUCT.value, _table_item(element_name))

        # Set rest of fields
        for col in self.TableColumns.product_data_indices():
            col_value = element[str(col)]
            self.recipe_contents.setItem(row_count, col.value, _table_item(col_value))

        self.update_total()

    def update_total(self):
        """ Updates info about total information. """
        total = {"mass": 0, "calories": 0, "protein": 0, "fat": 0, "carbohydrates": 0}
        for recipe_element in self.get_recipe().values():
            for key in total:
                total[key] += recipe_element[key]

        self.set_recipe_total_info(total)

    def get_recipe(self) -> Dict[str, Dict[str, float]]:
        """ Returns recipe as a list of dicts with data. """
        result = {}

        for row_idx in range(self.recipe_contents.rowCount()):
            entry = {}

            name = self.recipe_contents.item(row_idx, self.TableColumns.PRODUCT.value).text()

            for col in self.TableColumns.product_data_indices():
                element = self.recipe_contents.item(row_idx, col.value).text()
                entry[str(col)] = float(element)

            result[name] = entry

        return result
