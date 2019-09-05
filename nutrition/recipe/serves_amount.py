from typing import Optional

from PySide2.QtCore import Slot
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout
from PySide2.QtGui import QIntValidator

from .recipe_table import RecipeTableWidget


class ServesAmountWidget(QWidget):
    def __init__(self):
        super().__init__()
        serves_amount_label = QLabel("Количество порций:")

        serves_amount_line_edit = QLineEdit("1")
        serves_amount_line_edit.setFixedWidth(30)
        serves_amount_line_edit.setValidator(QIntValidator())
        serves_amount_line_edit.setMaxLength(2)

        serves_layout = QHBoxLayout()
        serves_layout.addWidget(serves_amount_label)
        serves_layout.addWidget(serves_amount_line_edit)

        self.setLayout(serves_layout)

        self.serves_amount_line_edit = serves_amount_line_edit
        self.recipe_table_widget: Optional[RecipeTableWidget] = None

    def serves(self) -> int:
        """ Returns the amount of serves entered in the line edit. """
        return int(self.serves_amount_line_edit.text())

    def set_recipe_table_widget(self, recipe_table_widget: RecipeTableWidget):
        """ Sets field to interact with recipe table module """
        self.recipe_table_widget = recipe_table_widget

        self._connect_serves_amount_slots()

    def _connect_serves_amount_slots(self):
        """ Connects slots associated with serves amount. """
        # Lint is disabled because pylint doesn't see .connect method
        # pylint: disable=no-member

        # Slot to be called when product name was entered.
        self.serves_amount_line_edit.editingFinished.connect(self._serves_amount_was_entered)

    @Slot()
    def _serves_amount_was_entered(self):
        if self.recipe_table_widget:
            self.recipe_table_widget.set_serves_amount(self.serves())
            self.recipe_table_widget.update_total()
