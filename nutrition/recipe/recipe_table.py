""" Module with the Recipe Table Widget. """

from typing import Dict, List, Union, Callable, Any, Optional
from enum import Enum
from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QTableWidget, QVBoxLayout, QTableWidgetItem

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

        def converter(self) -> Callable[[str], Any]:
            """ Returns a function to convert stored element into appropriate format. """

            converters = [str, int, float, float, float, float]

            return converters[self.value]

    def __init__(self):
        super().__init__()

        recipe_label = QLabel("Рецепт:")

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
        recipe_layout.addWidget(recipe_label)
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

    def add_recipe_element(self, element: Dict[str, Union[str, float]]):
        """ Adds a new row into recipe table with provided ingredient. """

        row_count = self.recipe_contents.rowCount()
        self.recipe_contents.insertRow(row_count)
        for col in self.TableColumns:
            col_value = element[str(col)]
            self.recipe_contents.setItem(row_count, col.value, _table_item(col_value))

        self.update_total()

    def update_total(self):
        """ Updates info about total information. """
        total = {"mass": 0, "calories": 0, "protein": 0, "fat": 0, "carbohydrates": 0}
        for recipe_element in self.get_recipe():
            for key in total:
                total[key] += recipe_element[key]

        self.set_recipe_total_info(total)

    def get_recipe(self) -> List[Dict[str, Union[str, float]]]:
        """ Returns recipe as a list of dicts with data. """
        result = []

        for row_idx in range(self.recipe_contents.rowCount()):
            entry = {}
            for col in self.TableColumns:
                converter = col.converter()
                element = self.recipe_contents.item(row_idx, col.value).text()
                entry[str(col)] = converter(element)

            result.append(entry)

        return result
