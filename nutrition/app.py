""" Main application. """

from typing import Dict
import logging
import sys
from PySide2.QtWidgets import QApplication, QWidget, QTabWidget

from .configuration import Configuration
from .recipe import RecipeWidget
from .recipe_manager import RecipeManager

# TODO make it configurable
logging.basicConfig(level=logging.DEBUG)


class NutritionApp(QWidget):
    """ Nutrition application. """

    def __init__(self, calories_data: Dict[str, Dict[str, float]]):
        super().__init__()

        # Main app settings
        self.title = "Nutrition application"
        self.left = 50
        self.top = 200
        self.width = 1000
        self.height = 1000
        self.calories_data = calories_data

        # Fields that will be inited during init_ui call
        self.recipe_widget = None

        # Init ui
        self.init_ui()

    def init_ui(self):
        """ Method to init UI. """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.recipe_widget = RecipeWidget(self.calories_data)

        self.tab_widget = QTabWidget(self)
        self.tab_widget.addTab(self.recipe_widget, "Рецепты")

        self.show()


def main(config_path: str):
    """ Main application runner. """
    config = Configuration(config_path)

    RecipeManager.set_path(config.recipes_folder())

    app = QApplication()
    _app = NutritionApp(config.calories_data())
    sys.exit(app.exec_())
