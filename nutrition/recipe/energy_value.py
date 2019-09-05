from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout


class EnergyValueWidget(QWidget):
    def __init__(self):
        super().__init__()

        energy_data_label = QLabel("Информация о продукте: ")
        energy_data_text = QLabel("")
        energy_data_text.setFixedWidth(300)

        # Layout for energy data
        energy_layout = QHBoxLayout()
        energy_layout.addWidget(energy_data_label)
        energy_layout.addWidget(energy_data_text)
        energy_layout.addStretch()

        self.setLayout(energy_layout)

        self.energy_data_text = energy_data_text

    def set_text(self, text):
        """ Sets text for the product info """
        self.energy_data_text.setText(text)
