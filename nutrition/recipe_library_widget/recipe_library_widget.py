""" Recipe library widget. """

from PySide2.QtWidgets import QWidget, QVBoxLayout

from nutrition.recipe import RecipeManager
from nutrition.logger import Logger

from .widgets.recipe_lookup import RecipeLookupWidget
from .widgets.recipe_content import RecipeContentWidget


class RecipeLibraryWidget(QWidget):
    """ Recipe library widget. """

    def __init__(self):
        super().__init__()

        recipe_names = RecipeManager().recipe_names()

        recipe_lookup_widget = RecipeLookupWidget(recipe_names, self._on_recipe_name_entered)
        recipe_content_widget = RecipeContentWidget()

        # Layout for the whole block.
        full_layout = QVBoxLayout()
        full_layout.addWidget(recipe_lookup_widget)
        full_layout.addWidget(recipe_content_widget)
        # full_layout.addStretch()

        self.setLayout(full_layout)

        # Init self data.
        self._recipe_names = set(recipe_names)
        self._recipe_content_widget = recipe_content_widget

    def _on_recipe_name_entered(self, recipe_name: str):
        if recipe_name not in self._recipe_names:
            # Incorrect recipe name, do nothing.
            return

        Logger.get_logger().debug("Succesfull lookup for a recipe %s", recipe_name)

        recipe = RecipeManager().load(recipe_name)
        self._recipe_content_widget.set_recipe(recipe)
