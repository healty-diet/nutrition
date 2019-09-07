""" Main application. """

from typing import Dict
import sys
from PySide2.QtWidgets import QApplication, QWidget, QTabWidget

from .configuration import Configuration
from .recipe_builder_widget import RecipeBuilderWidget
from .recipe_library_widget import RecipeLibraryWidget
from .recipe import RecipeManager
from .logger import Logger


class NutritionApp(QWidget):
    """ Nutrition application. """

    def __init__(self, calories_data: Dict[str, Dict[str, float]]):
        super().__init__()

        # Main app settings
        self._title = "Nutrition application"
        self._geometry = {"left": 50, "top": 200, "width": 1000, "height": 1000}
        self._calories_data = calories_data

        # Fields that will be inited during init_ui call
        self._tab_widget = None

        # Init ui
        self._init_ui()

    def _ui_geometry(self):
        return [self._geometry["left"], self._geometry["top"], self._geometry["width"], self._geometry["height"]]

    def _init_ui(self):
        """ Method to init UI. """
        self.setWindowTitle(self._title)
        self.setGeometry(*self._ui_geometry())

        recipe_builder_widget = RecipeBuilderWidget(self._calories_data)
        recipe_library_widget = RecipeLibraryWidget()

        self._tab_widget = QTabWidget(self)
        self._tab_widget.addTab(recipe_builder_widget, "Добавление рецептов")
        self._tab_widget.addTab(recipe_library_widget, "База рецептов")

        self.show()


def run_app(config_path: str):
    """ Main application runner. """
    config = Configuration(config_path)

    Logger.init_logger(config.logging_level())

    RecipeManager.set_path(config.recipes_folder())

    app = QApplication()
    _app = NutritionApp(config.calories_data())
    sys.exit(app.exec_())
