""" Tests for the recipe text widget. """

from PySide2.QtWidgets import QPlainTextEdit
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest

from nutrition.recipe_builder_widget.widgets.recipe_text import RecipeTextWidget

from tests.helpers import UsesQApplication, random_string


class TestRecipeTextWidget(UsesQApplication):
    """ Tests for the recipe text widget. """

    def test_recipe_text_has_textedit(self):
        """ Tests the widget layout. """
        widget = RecipeTextWidget()

        self.assertTrue(hasattr(widget, "widget"))
        self.assertTrue(isinstance(widget.widget, QPlainTextEdit))

    def test_recipe_get_text(self):
        """ Tests the get text method. """
        widget = RecipeTextWidget()

        input_data = [random_string(50) for _ in range(10)]

        for line in input_data:
            for char in line:
                QTest.keyPress(widget.widget, char)
                QTest.keyRelease(widget.widget, char)

            QTest.keyPress(widget.widget, Qt.Key.Key_Enter)
            QTest.keyRelease(widget.widget, Qt.Key.Key_Enter)

        self.assertEqual(widget.get_text(), "\n".join(input_data) + "\n")

