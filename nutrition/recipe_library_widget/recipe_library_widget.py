""" Recipe library widget. """

from PySide2.QtWidgets import QWidget, QVBoxLayout

from nutrition.recipe import RecipeManager

from .widgets.recipe_lookup import RecipeLookupWidget


class RecipeLibraryWidget(QWidget):
    """ Recipe library widget. """

    def __init__(self):
        super().__init__()

        recipe_names = RecipeManager().recipe_names()

        recipe_lookup_widget = RecipeLookupWidget(recipe_names, self._on_recipe_name_entered)

        # Layout for the whole block.
        full_layout = QVBoxLayout()
        full_layout.addWidget(recipe_lookup_widget)
        full_layout.addStretch()

        self.setLayout(full_layout)

        # Init self data.
        self._recipe_names = recipe_names

    def _on_recipe_name_entered(self):
        pass
