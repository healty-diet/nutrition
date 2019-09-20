""" Widget for ingredient adding. """

from typing import List, Callable
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QCompleter, QPushButton, QHBoxLayout
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QIntValidator

# from .utils import energy_data_str, scale

CallbackType = Callable[[str, int], None]


class IngredientWidget(QWidget):
    """ Widget that is capable of addint ingredients to the recipe. """

    # def __init__(self, calories_data: Dict[str, Union[str, float]]):
    def __init__(
        self, food_names: List[str], on_ingredient_entered: CallbackType, on_ingredient_finalized: CallbackType
    ) -> None:
        super().__init__()

        self._food_names = food_names
        self._on_ingredient_entered = on_ingredient_entered
        self._on_ingredient_finalized = on_ingredient_finalized

        # ingredient
        ingredient_label = QLabel("Продукт:")
        ingredient_line_edit = QLineEdit()

        # Completer for the ingredient line edit
        completer = QCompleter(self._food_names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        ingredient_line_edit.setCompleter(completer)

        # ingredient mass line edit
        ingredient_mass_line_edit = QLineEdit()
        ingredient_mass_line_edit.setPlaceholderText("Масса (гр.)")
        ingredient_mass_line_edit.setFixedWidth(100)
        ingredient_mass_line_edit.setValidator(QIntValidator())
        ingredient_mass_line_edit.setMaxLength(4)

        # Button to add ingredient to the recipe

        ingredient_add_button = QPushButton("+")

        # Layout for ingredient_label / ingredient_line_edit
        ingredient_layout = QHBoxLayout()
        ingredient_layout.addWidget(ingredient_label)
        ingredient_layout.addWidget(ingredient_line_edit)
        ingredient_layout.addWidget(ingredient_mass_line_edit)
        ingredient_layout.addWidget(ingredient_add_button)

        self.setLayout(ingredient_layout)

        self._ingredient_line_edit = ingredient_line_edit
        self._ingredient_mass_line_edit = ingredient_mass_line_edit
        self._ingredient_add_button = ingredient_add_button

        self._connect_slots()

    def _connect_slots(self) -> None:
        """ Connects slots associated with energy data. """
        # Lint is disabled because pylint doesn't see .connect method
        # pylint: disable=no-member

        self._ingredient_line_edit.editingFinished.connect(self._ingredient_name_entered)
        self._ingredient_mass_line_edit.editingFinished.connect(self._ingredient_mass_entered)
        self._ingredient_add_button.clicked.connect(self._add_ingredient_to_recipe)

    @Slot()
    def _ingredient_name_entered(self) -> None:
        """ Slot for the ingredient search. """
        ingredient = self._ingredient_line_edit.text()
        ingredient_mass_text = self._ingredient_mass_line_edit.text()
        if not ingredient_mass_text:
            ingredient_mass = 100
        else:
            ingredient_mass = int(ingredient_mass_text)

        self._on_ingredient_entered(ingredient, ingredient_mass)

    @Slot()
    def _ingredient_mass_entered(self) -> None:
        """ Slot to calculate energy values for entered mass. """

        ingredient = self._ingredient_line_edit.text()
        ingredient_mass = int(self._ingredient_mass_line_edit.text())

        self._on_ingredient_entered(ingredient, ingredient_mass)

    @Slot()
    def _add_ingredient_to_recipe(self) -> None:
        """ Slot for adding ingredient to the recipe. """
        ingredient = self._ingredient_line_edit.text()
        ingredient_mass = int(self._ingredient_mass_line_edit.text())

        self._on_ingredient_finalized(ingredient, ingredient_mass)
