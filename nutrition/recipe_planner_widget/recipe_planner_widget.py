""" Recipe planner widget. """

from PySide2.QtWidgets import QWidget, QVBoxLayout

from nutrition.logger import Logger
from nutrition.recipe import RecipeManager, Recipe

from .widgets.pool_item import PoolItemWidget
from .widgets.pool import PoolWidget


class RecipePlannerWidget(QWidget):
    """ Recipe planner widget. """

    def __init__(self):
        super().__init__()

        week_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        meals_amount = 5

        recipe_names = RecipeManager().recipe_names()

        pool_item_widget = PoolItemWidget(recipe_names, self._on_pool_item_added)
        pool_widget = PoolWidget(week_days, meals_amount, self._on_meal_planned)

        # Layout for the whole block.
        full_layout = QVBoxLayout()
        full_layout.addWidget(pool_item_widget)
        full_layout.addWidget(pool_widget)
        full_layout.addStretch()

        self.setLayout(full_layout)

        # Init self data.
        self._recipe_names = set(recipe_names)
        self._pool_widget = pool_widget

    def _on_pool_item_added(self, recipe_name: str, serves_amount: int):
        if recipe_name not in self._recipe_names:
            # Incomplete recipe name, do nothing.
            return

        Logger.get_logger().debug("Successfull lookup for a recipe %s", recipe_name)

        # _recipe = RecipeManager().load(recipe_name)
        self._pool_widget.add_meal(recipe_name, serves_amount)

        # TODO

    def _on_meal_planned(self, recipe_name: str, week_day: str, meal_idx: int):
        pass
