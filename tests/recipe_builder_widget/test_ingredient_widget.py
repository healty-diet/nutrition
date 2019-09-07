""" Tests for the ingredient widget. """

from PySide2.QtWidgets import QLineEdit, QPushButton
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest

from nutrition.recipe_builder_widget.widgets.ingredient import IngredientWidget

from tests.helpers import UsesQApplication, Callback, empty_callback


class TestIngredientWidget(UsesQApplication):
    """ Tests for the recipe name widget. """

    # This is a test, access to the private members is ok.
    # pylint: disable=protected-access

    PRODUCT_NAMES = ["test1", "test2", "test3"]

    def test_ingredient_layout(self):
        """ Tests the widget layout. """
        sample_callback = Callback()
        widget = IngredientWidget(self.PRODUCT_NAMES, empty_callback, empty_callback)

        self.assertTrue(hasattr(widget, "_ingredient_line_edit"))
        self.assertTrue(isinstance(widget._ingredient_line_edit, QLineEdit))

        self.assertTrue(hasattr(widget, "_ingredient_mass_line_edit"))
        self.assertTrue(isinstance(widget._ingredient_mass_line_edit, QLineEdit))

        self.assertTrue(hasattr(widget, "_ingredient_add_button"))
        self.assertTrue(isinstance(widget._ingredient_add_button, QPushButton))

    def test_ingredient_entered(self):
        """ Tests that after entering ingredient name the first callback is called. """
        input_data = self.PRODUCT_NAMES[0]
        default_mass = 100

        ingredient_entered_callback = Callback((input_data, default_mass))
        finalize_callback = Callback()
        widget = IngredientWidget(self.PRODUCT_NAMES, ingredient_entered_callback.callback, finalize_callback.callback)

        for char in input_data:
            QTest.keyPress(widget._ingredient_line_edit, char)
            QTest.keyRelease(widget._ingredient_line_edit, char)

        QTest.keyPress(widget._ingredient_line_edit, Qt.Key.Key_Enter)
        QTest.keyRelease(widget._ingredient_line_edit, Qt.Key.Key_Enter)

        self.assertTrue(ingredient_entered_callback.called)
        self.assertFalse(finalize_callback.called)

    def test_ingredient_mass_entered(self):
        """ Tests that after entering ingredient mass the first callback is called. """
        input_data = "259"

        ingredient_entered_callback = Callback(("", int(input_data)))
        finalize_callback = Callback()
        widget = IngredientWidget(self.PRODUCT_NAMES, ingredient_entered_callback.callback, finalize_callback.callback)

        for char in input_data:
            QTest.keyPress(widget._ingredient_mass_line_edit, char)
            QTest.keyRelease(widget._ingredient_mass_line_edit, char)

        QTest.keyPress(widget._ingredient_mass_line_edit, Qt.Key.Key_Enter)
        QTest.keyRelease(widget._ingredient_mass_line_edit, Qt.Key.Key_Enter)

        self.assertTrue(ingredient_entered_callback.called)
        self.assertFalse(finalize_callback.called)

    def test_ingredient_name_and_mass_entered(self):
        """ Tests that after entering ingredient name and mass the first callback is called. """
        input_data_name = self.PRODUCT_NAMES[1]
        input_data_mass = "331"
        default_mass = 100

        # After the first call (after product name was entered) the mass will be equal to default_mass.
        ingredient_entered_callback = Callback((input_data_name, default_mass))
        finalize_callback = Callback()
        widget = IngredientWidget(self.PRODUCT_NAMES, ingredient_entered_callback.callback, finalize_callback.callback)

        for char in input_data_name:
            QTest.keyPress(widget._ingredient_line_edit, char)
            QTest.keyRelease(widget._ingredient_line_edit, char)

        QTest.keyPress(widget._ingredient_line_edit, Qt.Key.Key_Enter)
        QTest.keyRelease(widget._ingredient_line_edit, Qt.Key.Key_Enter)

        # Refresh the callback.
        ingredient_entered_callback.called = False
        ingredient_entered_callback.expected_args = (input_data_name, int(input_data_mass))

        for char in input_data_mass:
            QTest.keyPress(widget._ingredient_mass_line_edit, char)
            QTest.keyRelease(widget._ingredient_mass_line_edit, char)

        QTest.keyPress(widget._ingredient_mass_line_edit, Qt.Key.Key_Enter)
        QTest.keyRelease(widget._ingredient_mass_line_edit, Qt.Key.Key_Enter)

        self.assertTrue(ingredient_entered_callback.called)
        self.assertFalse(finalize_callback.called)

    def test_ingredient_name_and_mass_finalize(self):
        """ Tests that after clicking the finalize button the second callback is called. """
        input_data_name = self.PRODUCT_NAMES[1]
        input_data_mass = "331"

        # After the first call (after product name was entered) the mass will be equal to 100.
        ingredient_entered_callback = Callback((input_data_name, 100))
        finalize_callback = Callback((input_data_name, int(input_data_mass)))
        widget = IngredientWidget(self.PRODUCT_NAMES, ingredient_entered_callback.callback, finalize_callback.callback)

        for char in input_data_name:
            QTest.keyPress(widget._ingredient_line_edit, char)
            QTest.keyRelease(widget._ingredient_line_edit, char)

        QTest.keyPress(widget._ingredient_line_edit, Qt.Key.Key_Enter)
        QTest.keyRelease(widget._ingredient_line_edit, Qt.Key.Key_Enter)

        # Refresh the callback.
        ingredient_entered_callback.called = False
        ingredient_entered_callback.expected_args = (input_data_name, int(input_data_mass))

        for char in input_data_mass:
            QTest.keyPress(widget._ingredient_mass_line_edit, char)
            QTest.keyRelease(widget._ingredient_mass_line_edit, char)

        QTest.keyPress(widget._ingredient_mass_line_edit, Qt.Key.Key_Enter)
        QTest.keyRelease(widget._ingredient_mass_line_edit, Qt.Key.Key_Enter)

        QTest.mouseClick(widget._ingredient_add_button, Qt.MouseButton.LeftButton)

        self.assertTrue(finalize_callback.called)
