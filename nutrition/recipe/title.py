from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout


class TitleWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Title label
        title_label = QLabel("Добавление рецепта")

        title_layout = QHBoxLayout()
        title_layout.addWidget(title_label)

        self.setLayout(title_layout)
