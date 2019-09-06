""" Module with the Recipe Table Widget. """

from typing import List
from enum import Enum
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem

from nutrition.recipe_manager.energy_value import EnergyValue


def _table_item(value):
    """ Returns QTableWidgetItem with the string as value. """

    return QTableWidgetItem(str(value))


class RecipeTableWidget(QTableWidget):
    """
    Widget that is capable of handling the recipe itself.
    It contains the table with the ingredients and the field with total recipe energy value.
    """

    class TableColumns(Enum):
        """ Enum for describing table columns. """

        # Lint is disabled because pylint doesn't recognize Enum's .value attribute
        # pylint: disable=invalid-sequence-index

        INGREDIENT_NAME = 0
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
        def product_data_indices(cls) -> List["RecipeTableWidget.TableColumns"]:
            """ Returns indices for product data fields. """
            return [cls(idx) for idx in range(cls.MASS.value, cls.CARBOHYDRATES.value + 1)]

    def __init__(self):
        columns = [el.translated_str() for el in self.TableColumns]

        super().__init__(0, len(columns))
        self.setHorizontalHeaderLabels(columns)
        self.setFixedWidth(700)
        self.horizontalHeader().setDefaultSectionSize(50)
        self.setColumnWidth(self.TableColumns.INGREDIENT_NAME.value, 350)

    def add_ingredient(self, ingredient_name: str, energy_value: EnergyValue, ingredient_mass: int):
        """ Adds a new row into recipe table with provided ingredient. """

        row_count = self.rowCount()
        self.insertRow(row_count)

        # Set name
        self.setItem(row_count, self.TableColumns.INGREDIENT_NAME.value, _table_item(ingredient_name))
        self.setItem(row_count, self.TableColumns.MASS.value, _table_item(ingredient_mass))
        self.setItem(row_count, self.TableColumns.CALORIES.value, _table_item(energy_value.calories))
        self.setItem(row_count, self.TableColumns.PROTEIN.value, _table_item(energy_value.protein))
        self.setItem(row_count, self.TableColumns.FAT.value, _table_item(energy_value.fat))
        self.setItem(row_count, self.TableColumns.CARBOHYDRATES.value, _table_item(energy_value.carbohydrates))
