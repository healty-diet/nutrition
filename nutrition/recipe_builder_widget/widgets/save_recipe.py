""" Module with the Recipe Text Widget. """

from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide2.QtCore import Slot


class SaveRecipeWidget(QWidget):
    """
    Widget that is capable of saving the recipe.
    """

    def __init__(self, on_clicked):
        self._on_clicked = on_clicked

        super().__init__()

        save_button = QPushButton("Сохранить рецепт")

        # Layout for the save block

        save_layout = QVBoxLayout()
        save_layout.addWidget(save_button)
        save_layout.addStretch()

        self.setLayout(save_layout)

        self._save_button = save_button
        self._connect_slots()

    def _connect_slots(self):
        # Lint is disabled because pylint doesn't see .connect method
        # pylint: disable=no-member
        self._save_button.clicked.connect(self._save_button_clicked)

    @Slot()
    def _save_button_clicked(self, _checked):
        self._on_clicked()
