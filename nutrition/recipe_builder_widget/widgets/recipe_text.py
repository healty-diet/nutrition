""" Module with the Recipe Text Widget. """

from PySide2.QtWidgets import QPlainTextEdit

from nutrition.utils import WidgetWithLabel


class RecipeTextWidget(WidgetWithLabel):
    """
    Widget that is capable of handling the recipe steps.
    """

    def __init__(self) -> None:
        recipe_text = QPlainTextEdit()

        super().__init__("Приготовление:", recipe_text, layout=WidgetWithLabel.Layout.VERTICAL)

    def get_text(self) -> str:
        """ Returns stored text. """
        return self.widget.toPlainText()
