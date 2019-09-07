""" Tests for the recipe name widget. """

from PySide2.QtWidgets import QLineEdit
from PySide2.QtTest import QTest

from nutrition.recipe_builder_widget.widgets.recipe_name import RecipeNameWidget

from tests.helpers import UsesQApplication, random_string


class TestRecipeNameWidget(UsesQApplication):
    """ Tests for the recipe name widget. """

    def test_recipe_name_has_lineedit(self):
        """ Tests the widget layout. """
        widget = RecipeNameWidget()

        self.assertTrue(hasattr(widget, "widget"))
        self.assertTrue(isinstance(widget.widget, QLineEdit))

    def test_recipe_name(self):
        """ Tests the name method. """
        widget = RecipeNameWidget()

        input_data = random_string()

        for char in input_data:
            QTest.keyPress(widget.widget, char)
            QTest.keyRelease(widget.widget, char)

        self.assertEqual(widget.name(), input_data)

