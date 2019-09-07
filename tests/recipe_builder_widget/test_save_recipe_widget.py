""" Tests for the save recipe widget. """

from PySide2.QtWidgets import QPushButton
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest

from nutrition.recipe_builder_widget.widgets.save_recipe import SaveRecipeWidget

from tests.helpers import UsesQApplication, Callback, empty_callback


class TestSaveRecipeWidget(UsesQApplication):
    """ Tests for the serves amount widget. """

    # This is a test, access to the private members is ok.
    # pylint: disable=protected-access

    def test_serves_amount_has_pushbutton(self):
        """ Tests the widget layout. """
        widget = SaveRecipeWidget(empty_callback)

        self.assertTrue(hasattr(widget, "_save_button"))
        self.assertTrue(isinstance(widget._save_button, QPushButton))

    def test_callback(self):
        """ Tests that callback is called when button is clicked. """
        callback = Callback()
        widget = SaveRecipeWidget(callback.callback)

        QTest.mouseClick(widget._save_button, Qt.MouseButton.LeftButton)

        self.assertTrue(callback.called)
