""" Module with the Plan Widget. """

from typing import List, Any, Optional, Tuple, Dict
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide2.QtCore import Slot

# from nutrition.recipe.energy_value import EnergyValue


def _table_item(value: Any) -> QTableWidgetItem:
    """ Returns QTableWidgetItem with the string as value. """

    return QTableWidgetItem(str(value))


class PlanWidget(QTableWidget):
    """
    Widget that is capable of handling the nutrition plan.
    """

    def __init__(self, week_days: List[str], meals_amount: int) -> None:
        self._week_days = week_days
        self._meals_amount = meals_amount

        # One column for each day and one additional for calories.
        columns_amount = len(week_days) * 2
        column_header_labels = ["ккал"] * columns_amount
        for day in week_days:
            column_header_labels[self._day_column(day)] = day

        super().__init__(meals_amount + 1, len(week_days) * 2)
        self.setHorizontalHeaderLabels(column_header_labels)
        self.setVerticalHeaderLabels([str(i) for i in range(1, meals_amount + 1)] + ["#"])
        self.setFixedWidth(915)
        self.setWordWrap(True)

        horizontal_header = self.horizontalHeader()
        horizontal_header.setDefaultSectionSize(20)
        for day in week_days:
            day_column = self._day_column(day)
            logical_idx = horizontal_header.logicalIndexAt(day_column)
            horizontal_header.setSectionResizeMode(logical_idx, QHeaderView.Stretch)
            self.setColumnWidth(day_column, 90)

        self._connect_slots()

        self.resizeRowsToContents()

    def _connect_slots(self) -> None:
        # Lint is disabled because pylint doesn't see .connect method
        # pylint: disable=no-member
        self.cellChanged.connect(self._cell_changed)

    @Slot()
    def _cell_changed(self, row: int, _column: int) -> None:
        self.resizeRowToContents(row)

    def _day_column(self, day: str) -> int:
        return self._week_days.index(day) * 2

    def _calories_column(self, day: str) -> int:
        return self._day_column(day) + 1

    def _recalculate_day(self, day: str) -> None:
        calories_column = self._calories_column(day)

        sum_calories = 0

        for row in range(self._meals_amount):
            item = self.item(row, calories_column)

            if item is None:
                # That meal is not planned yet.
                continue

            calories = int(item.text())

            sum_calories += calories

        self.setItem(self._meals_amount, calories_column, _table_item(sum_calories))

    def add_meal(self, meal_name: str, day: str, meal_idx: int, calories: int) -> Optional[str]:
        """Adds meal to the plan."""
        meal_column = self._day_column(day)
        calories_column = self._calories_column(day)
        row = meal_idx - 1  # Meal indices starting from one.

        current_item = self.item(row, meal_column)
        # Get replaced meal name (if any).
        if current_item:
            replaced = current_item.text()
        else:
            replaced = None

        self.setItem(row, meal_column, _table_item(meal_name))
        self.setItem(row, calories_column, _table_item(calories))

        self._recalculate_day(day)

        return replaced

    def get_plan(self) -> Dict[str, List[Tuple[str, str, str]]]:
        """ Returns the created plan. """
        result: Dict[str, List[Tuple[str, str, str]]] = dict()

        for day in self._week_days:
            result[day] = []

            meal_column = self._day_column(day)
            calories_column = self._calories_column(day)
            for row in range(self._meals_amount):
                number = str(row + 1)
                meal_item = self.item(row, meal_column)
                if meal_item:
                    meal_name = meal_item.text()
                else:
                    meal_name = ""
                calories_item = self.item(row, calories_column)
                if calories_item:
                    calories = calories_item.text()
                else:
                    calories = ""

                result[day].append((number, meal_name, calories))

            overall_calories_item = self.item(self._meals_amount, calories_column)
            if overall_calories_item:
                overall_calories = overall_calories_item.text()
            else:
                overall_calories = ""

            result[day].append(("#", "", overall_calories))

        return result
