""" Widget with the name of the recipe. """
from PySide2.QtWidgets import QLineEdit

from nutrition.utils import WidgetWithLabel


class RecipeNameWidget(WidgetWithLabel):
    """ Widget with the name of the recipe. """

    def __init__(self) -> None:
        name_line_edit = QLineEdit()

        super().__init__("Название рецепта:", name_line_edit)

    def name(self) -> str:
        """ Returns the name of the recipe. """
        return self.widget.text()
