""" Module with the Recipe Text Widget. """

from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton


class SaveRecipeWidget(QWidget):
    """
    Widget that is capable of saving the recipe.
    """

    def __init__(self):
        super().__init__()

        save_button = QPushButton("Сохранить рецепт")

        # Layout for the save block

        save_layout = QVBoxLayout()
        save_layout.addWidget(save_button)
        save_layout.addStretch()

        self.setLayout(save_layout)
