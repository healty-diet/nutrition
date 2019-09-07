""" Tests for the serves amount widget. """

from PySide2.QtWidgets import QLineEdit
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest

from nutrition.recipe_builder_widget.widgets.serves_amount import ServesAmountWidget

from tests.helpers import UsesQApplication, Callback, empty_callback


class TestServesAmountWidget(UsesQApplication):
    """ Tests for the serves amount widget. """

    def test_serves_amount_has_lineedit(self):
        """ Tests the widget layout. """
        widget = ServesAmountWidget(empty_callback)

        self.assertTrue(hasattr(widget, "widget"))
        self.assertTrue(isinstance(widget.widget, QLineEdit))

    def test_serves(self):
        """ Tests the name method. """
        widget = ServesAmountWidget(empty_callback)

        input_data = "5"

        QTest.keyPress(widget.widget, Qt.Key.Key_Backspace)
        QTest.keyRelease(widget.widget, Qt.Key.Key_Backspace)

        for char in input_data:
            QTest.keyPress(widget.widget, char)
            QTest.keyRelease(widget.widget, char)

        QTest.keyPress(widget.widget, Qt.Key.Key_Enter)
        QTest.keyRelease(widget.widget, Qt.Key.Key_Enter)

        self.assertEqual(widget.serves(), int(input_data))

    def test_serves_callback(self):
        """ Tests that callback is called when value is entered. """
        callback = Callback((5,))
        widget = ServesAmountWidget(callback.callback)

        input_data = "5"

        QTest.keyPress(widget.widget, Qt.Key.Key_Backspace)
        QTest.keyRelease(widget.widget, Qt.Key.Key_Backspace)

        for char in input_data:
            QTest.keyPress(widget.widget, char)
            QTest.keyRelease(widget.widget, char)

        QTest.keyPress(widget.widget, Qt.Key.Key_Enter)
        QTest.keyRelease(widget.widget, Qt.Key.Key_Enter)

        self.assertTrue(callback.called)
