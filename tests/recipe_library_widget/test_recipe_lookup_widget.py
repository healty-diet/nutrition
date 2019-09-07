""" Tests for the recipe lookup widget. """

from PySide2.QtWidgets import QLineEdit
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest

from nutrition.recipe_library_widget.widgets.recipe_lookup import RecipeLookupWidget

from tests.helpers import UsesQApplication, Callback, empty_callback


class TestRecipeLookupWidget(UsesQApplication):
    """ Tests for the recipe lookup widget. """

    def test_recipe_lookup_has_textedit(self):
        """ Tests the widget layout. """
        widget = RecipeLookupWidget([], empty_callback)

        self.assertTrue(hasattr(widget, "widget"))
        self.assertTrue(isinstance(widget.widget, QLineEdit))

    def test_recipe_lookup_callback(self):
        """ Tests the get text method. """
        product_names = ["test1", "test2", "test3"]
        callback = Callback(("test2",))

        widget = RecipeLookupWidget(product_names, callback.callback)

        input_data = "test2"

        for char in input_data:
            QTest.keyPress(widget.widget, char)
            QTest.keyRelease(widget.widget, char)

        QTest.keyPress(widget.widget, Qt.Key.Key_Enter)
        QTest.keyRelease(widget.widget, Qt.Key.Key_Enter)

        self.assertTrue(callback.called)
