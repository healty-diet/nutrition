""" Serves amount widget. """
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QLineEdit
from PySide2.QtGui import QIntValidator

from nutrition.utils import WidgetWithLabel


class ServesAmountWidget(WidgetWithLabel):
    """ Widget that holds amount of serves. """

    def __init__(self, on_serves_entered):
        self._on_serves_entered = on_serves_entered

        serves_amount_line_edit = QLineEdit("1")
        serves_amount_line_edit.setFixedWidth(30)
        serves_amount_line_edit.setValidator(QIntValidator())
        serves_amount_line_edit.setMaxLength(2)

        super().__init__("Количество порций:", serves_amount_line_edit)

        self._connect_slots()

    def serves(self) -> int:
        """ Returns the amount of serves entered in the line edit. """
        return int(self.widget.text())

    def _connect_slots(self):
        """ Connects slots associated with serves amount. """
        # Lint is disabled because pylint doesn't see .connect method
        # pylint: disable=no-member

        # Slot to be called when product name was entered.
        self.widget.editingFinished.connect(self._serves_amount_was_entered)

    @Slot()
    def _serves_amount_was_entered(self):
        self._on_serves_entered(self.serves())
