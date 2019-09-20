""" Recipe planner widget. """

from PySide2.QtWidgets import QWidget, QVBoxLayout, QFileDialog

import xlwt

from nutrition.logger import Logger
from nutrition.recipe import RecipeManager
from nutrition.utils import SaveButtonWidget

from .widgets.pool_item import PoolItemWidget
from .widgets.pool import PoolWidget
from .widgets.plan import PlanWidget
from .widgets.shopping_list import ShoppingListWidget


class RecipePlannerWidget(QWidget):
    """ Recipe planner widget. """

    def __init__(self) -> None:
        super().__init__()

        # TODO make it configurable.
        week_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        meals_amount = 5

        recipe_names = RecipeManager().recipe_names()

        pool_item_widget = PoolItemWidget(recipe_names, self._on_pool_item_added)
        pool_widget = PoolWidget(week_days, meals_amount, self._on_meal_planned)
        plan_widget = PlanWidget(week_days, meals_amount)
        shopping_list_widget = ShoppingListWidget()
        save_plan_widget = SaveButtonWidget("Сохранить меню", self._on_save)

        # Layout for the whole block.
        full_layout = QVBoxLayout()
        full_layout.addWidget(pool_item_widget)
        full_layout.addWidget(pool_widget)
        full_layout.addWidget(plan_widget)
        full_layout.addWidget(shopping_list_widget)
        full_layout.addWidget(save_plan_widget)
        full_layout.addStretch()

        self.setLayout(full_layout)

        # Init self data.
        self._week_days = week_days
        self._recipe_names = set(recipe_names)
        self._pool_widget = pool_widget
        self._plan_widget = plan_widget
        self._shopping_list_widget = shopping_list_widget

    def _on_pool_item_added(self, recipe_name: str, serves_amount: int) -> None:
        if recipe_name not in self._recipe_names:
            # Incomplete recipe name, do nothing.
            return

        Logger.get_logger().debug("Successfull lookup for a recipe %s", recipe_name)

        self._pool_widget.add_meal(recipe_name, serves_amount)

    def _on_meal_planned(self, recipe_name: str, week_day: str, meal_idx: int) -> None:
        recipe = RecipeManager().load(recipe_name)

        calories = recipe.energy_value_per_serving.calories

        replaced_name = self._plan_widget.add_meal(recipe_name, week_day, meal_idx, int(calories))

        for ingredient in recipe.ingredients_per_serving():
            name = list(ingredient.keys())[0]
            self._shopping_list_widget.add_ingredient(name, ingredient[name])

        if replaced_name is not None:
            self._pool_widget.add_meal(replaced_name, 1)

            old_recipe = RecipeManager().load(replaced_name)
            for ingredient in old_recipe.ingredients_per_serving():
                name = list(ingredient.keys())[0]
                self._shopping_list_widget.remove_ingredient(name, ingredient[name])

    def _on_save(self) -> None:
        file_path = QFileDialog.getSaveFileName(self, "Сохранить как", filter="Файлы Excel (*.xls)")[0]
        if not file_path.endswith(".xls"):
            file_path += ".xls"

        # TODO move xls creation into separate module.

        workbook = xlwt.Workbook()

        self._build_plan_sheet(workbook)
        self._build_shopping_list_sheet(workbook)

        workbook.save(file_path)

    def _build_plan_sheet(self, workbook: xlwt.Workbook) -> None:
        plan = self._plan_widget.get_plan()

        plan_sheet = workbook.add_sheet("Меню")
        plan_sheet.col(1).width = 10000
        first_row = 0
        for week_day in self._week_days:
            first_column = 0
            plan_sheet.write(first_row, first_column, week_day)

            for meal_idx, (header, name, calories) in enumerate(plan[week_day]):
                meal_idx += 1  # Because it was taken
                plan_sheet.write(first_row + meal_idx, first_column, header)
                plan_sheet.write(first_row + meal_idx, first_column + 1, name)
                plan_sheet.write(first_row + meal_idx, first_column + 2, calories)

            first_row += len(plan[week_day]) + 2

    def _build_shopping_list_sheet(self, workbook: xlwt.Workbook) -> None:
        shopping_list = self._shopping_list_widget.get_shopping_list()

        shopping_list_sheet = workbook.add_sheet("Список покупок")
        for idx, ingredient in enumerate(shopping_list):
            shopping_list_sheet.write(idx, 0, ingredient)
            measure_offset = 1
            for measure_idx, measure_name in enumerate(shopping_list[ingredient]):
                amount_str = "{:.2f} ({})".format(shopping_list[ingredient][measure_name], measure_name)
                shopping_list_sheet.write(idx, measure_offset + measure_idx, amount_str)
