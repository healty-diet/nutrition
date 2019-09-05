""" Main application. """

from typing import Dict
import logging
import sys
import json
from PySide2.QtWidgets import QApplication, QWidget, QTabWidget

from recipe import RecipeWidget

# TODO store in config
CALORIES_DB_PATH = "../../../calories.json"

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
        self.width = 1366
        self.height = 768
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


def main():
    """ Main application runner. """
    app = QApplication(sys.argv)
    with open(CALORIES_DB_PATH) as file:
        calories_data = json.load(file)
    _app = NutritionApp(calories_data)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
