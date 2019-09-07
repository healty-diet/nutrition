""" Recipe content widget. """

from PySide2.QtWidgets import QPlainTextEdit

from nutrition.recipe import Recipe


class RecipeContentWidget(QPlainTextEdit):
    """ Recipe content widget. """

    def __init__(self):
        super().__init__()

        self.setReadOnly(True)

    def set_recipe(self, recipe: Recipe):
        self.setPlainText(recipe.as_json())
