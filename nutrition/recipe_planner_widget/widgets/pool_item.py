""" Pool item widget. """

from typing import Callable, List

from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QPushButton, QCompleter
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QIntValidator

CallbackType = Callable[[str, int], None]


class PoolItemWidget(QWidget):
    """ Pool item widget. """

    DEFAULT_SERVES_AMOUNT = 4

    def __init__(self, lookup_names: List, on_item_added: CallbackType) -> None:
        super().__init__()

        recipe_search_label = QLabel("Блюдо:")

        recipe_search_line_edit = QLineEdit("")
        completer = QCompleter(lookup_names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setMaxVisibleItems(50)
        recipe_search_line_edit.setCompleter(completer)

        serves_amount_label = QLabel("Порций:")

        serves_amount_line_edit = QLineEdit(str(self.DEFAULT_SERVES_AMOUNT))
        serves_amount_line_edit.setFixedWidth(30)
        serves_amount_line_edit.setValidator(QIntValidator())
        serves_amount_line_edit.setMaxLength(2)

        add_push_button = QPushButton("+")

        # Widget layout
        layout = QHBoxLayout()
        layout.addWidget(recipe_search_label)
        layout.addWidget(recipe_search_line_edit)
        layout.addWidget(serves_amount_label)
        layout.addWidget(serves_amount_line_edit)
        layout.addWidget(add_push_button)
        layout.addStretch()

        self.setLayout(layout)

        # Init self data
        self._on_item_added = on_item_added
        self._recipe_search_line_edit = recipe_search_line_edit
        self._serves_amount_line_edit = serves_amount_line_edit
        self._add_push_button = add_push_button

        # Connect slots
        self._connect_slots()

    def _connect_slots(self) -> None:
        # Lint is disabled because pylint doesn't see .connect method
        # pylint: disable=no-member
        self._add_push_button.clicked.connect(self._item_completed)

    @Slot()
    def _item_completed(self, _checked: bool) -> None:
        """ Slot for the recipe search. """
        recipe_name = self._recipe_search_line_edit.text()
        serves_amount = int(self._serves_amount_line_edit.text())

        self._on_item_added(recipe_name, serves_amount)

        self._recipe_search_line_edit.setText("")
        self._serves_amount_line_edit.setText(str(self.DEFAULT_SERVES_AMOUNT))
