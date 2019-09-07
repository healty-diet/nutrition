""" Recipe lookup widget. """

from PySide2.QtWidgets import QLineEdit, QCompleter
from PySide2.QtCore import Qt, Slot

from nutrition.utils import WidgetWithLabel


class RecipeLookupWidget(WidgetWithLabel):
    """ Recipe lookup widget. """

    def __init__(self, lookup_names, on_entered):
        widget = QLineEdit("")
        completer = QCompleter(lookup_names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        widget.setCompleter(completer)

        super().__init__("Название рецепта:", widget)

        self._on_recipe_name_entered = on_entered
        self._connect_slots()

    def _connect_slots(self):
        # Lint is disabled because pylint doesn't see .connect method
        # pylint: disable=no-member
        self.widget.editingFinished.connect(self._recipe_name_entered)

    @Slot()
    def _recipe_name_entered(self):
        """ Slot for the recipe search. """
        recipe_name = self.widget.text()

        self._on_recipe_name_entered(recipe_name)
