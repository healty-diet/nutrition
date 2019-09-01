""" Main application. """

from typing import Dict
import logging
import sys
import json
from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QCompleter,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QTabWidget,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
)

# TODO store in config
CALORIES_DB_PATH = "../../../calories.json"

# TODO make it configurable
logging.basicConfig(level=logging.DEBUG)


class NutritionApp(QWidget):
    """ Nutrition application. """

    def __init__(self, calories_data: Dict[str, Dict[str, float]]):
        super().__init__()

        # Main app settings
        self.title = "Nutrition application"
        self.left = 50
        self.top = 200
        self.width = 1366
        self.height = 768
        self.calories_data = calories_data
        self.calories_word_list = list(self.calories_data.keys())

        # Fields that will be inited during init_ui call
        self.product_line_edit = None
        self.product_mass_line_edit = None
        self.energy_data_text = None
        self.recipe_contents = None
        self.recipe_total_info_label = None

        # Init ui
        self.init_ui()

    def init_ui(self):
        """ Method to init UI. """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.recipe_widget = self.build_recipe_widget()

        self.tab_widget = QTabWidget(self)
        self.tab_widget.addTab(self.recipe_widget, "Рецепты")

        self.show()

    def build_recipe_widget(self):
        """ Builds recipe widget. """
        # Title label
        title_label = QLabel("Добавление рецепта")

        title_layout = QHBoxLayout()
        title_layout.addWidget(title_label)

        title_widget = QWidget()
        title_widget.setLayout(title_layout)

        # Serves amount
        serves_amount = QLabel("Количество порций:")

        serves_line_edit = QLineEdit("1")
        serves_line_edit.setInputMask("9")  # Only numbers allowed

        # Product
        product_label = QLabel("Продукт:")
        product_line_edit = QLineEdit()

        # Completer for the product line edit
        completer = QCompleter(self.calories_word_list, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        product_line_edit.setCompleter(completer)
        product_line_edit.editingFinished.connect(self.product_editing_finished)

        # Product mass line edit
        product_mass_line_edit = QLineEdit()
        product_mass_line_edit.setPlaceholderText("Масса (гр.)")
        product_mass_line_edit.editingFinished.connect(self.product_mass_editing_finished)
        product_mass_line_edit.setFixedWidth(100)
        product_mass_line_edit.setInputMask("9")  # Only numbers allowed

        # Button to add product to the recipe

        product_add = QPushButton("+")
        product_add.clicked.connect(self.product_add_clicked)

        # Layout for product_label / product_line_edit
        product_layout = QHBoxLayout()
        product_layout.addWidget(product_label)
        product_layout.addWidget(product_line_edit)
        product_layout.addWidget(product_mass_line_edit)
        product_layout.addWidget(product_add)

        product_widget = QWidget()
        product_widget.setLayout(product_layout)

        # Energy block

        energy_data_label = QLabel("Информация о продукте: ")
        energy_data_text = QLabel("")
        energy_data_text.setFixedWidth(300)

        # Layout for energy data
        energy_layout = QHBoxLayout()
        energy_layout.addWidget(energy_data_label)
        energy_layout.addWidget(energy_data_text)
        energy_layout.addStretch()

        energy_widget = QWidget()
        energy_widget.setLayout(energy_layout)

        # Recipe block

        recipe_label = QLabel("Рецепт:")

        columns = ["Продукт", "Масса", "К", "Б", "Ж", "У", "-"]
        recipe_contents = QTableWidget(0, len(columns))
        recipe_contents.setHorizontalHeaderLabels(columns)
        recipe_contents.setFixedWidth(700)
        recipe_contents.horizontalHeader().setDefaultSectionSize(50)
        recipe_contents.setColumnWidth(0, 350)

        recipe_total_label = QLabel("Итого:")
        recipe_total_info_label = QLabel("")
        recipe_total_info_label.setFixedWidth(300)

        recipe_total_layout = QHBoxLayout()
        recipe_total_layout.addWidget(recipe_total_label)
        recipe_total_layout.addWidget(recipe_total_info_label)
        recipe_total_layout.addStretch()

        recipe_total_widget = QWidget()
        recipe_total_widget.setLayout(recipe_total_layout)

        recipe_complete_button = QPushButton("Сохранить рецепт")

        # Layout for the recipe block

        recipe_layout = QVBoxLayout()
        recipe_layout.addWidget(recipe_label)
        recipe_layout.addWidget(recipe_contents)
        recipe_layout.addWidget(recipe_total_label)
        recipe_layout.addWidget(recipe_total_widget)
        recipe_layout.addWidget(recipe_complete_button)
        recipe_layout.addStretch()

        recipe_widget = QWidget()
        recipe_widget.setLayout(recipe_layout)

        # Layout for the whole block
        full_layout = QVBoxLayout()
        full_layout.addWidget(title_widget)
        full_layout.addWidget(product_widget)
        full_layout.addWidget(energy_widget)
        full_layout.addWidget(recipe_widget)

        widget = QWidget()
        widget.setLayout(full_layout)

        # Add required fields to self
        self.product_line_edit = product_line_edit
        self.product_mass_line_edit = product_mass_line_edit
        self.energy_data_text = energy_data_text
        self.recipe_contents = recipe_contents
        self.recipe_total_info_label = recipe_total_info_label

        return widget

    def scale(self, data_arr, scale_factor):
        """ Scales energy values for a given mass. """

        modifier = float(scale_factor) / 100.0

        return map(lambda el: float(el) * modifier, data_arr)

    def energy_data_str(self, energy_data, scale=False, product_mass=100):
        """ Takes energy data, scales it and returns as a string. """

        data = self.energy_data_dict_to_list(energy_data)

        if scale:
            data = self.scale(data, scale_factor=product_mass)

        return "К {:.1f} Б {:.1f} Ж {:.1f} У {:.1f} [на {} грамм]".format(*data, product_mass)

    def energy_data_dict_to_list(self, product_data):
        """ Makes dict with energy data a list. """

        return [product_data["calories"], product_data["protein"], product_data["fat"], product_data["carbohydrates"]]

    @Slot()
    def product_editing_finished(self):
        """ Slot for the product search. """
        product = self.product_line_edit.text()

        product_data = self.calories_data.get(product)
        if product_data:
            logging.debug("Completed product lookup: %s", product)

            energy_data_str = self.energy_data_str(product_data)

            self.energy_data_text.setText(energy_data_str)

    @Slot()
    def product_mass_editing_finished(self):
        """ Slot to calculate energy values for entered mass. """

        product = self.product_line_edit.text()
        product_mass = self.product_mass_line_edit.text()

        product_data = self.calories_data.get(product)
        if not product_data or not product_mass.isdigit():
            # Incorrect data, do nothing
            return

        logging.debug("Completed product lookup with mass: %s / %s", product, product_mass)

        energy_data_str = self.energy_data_str(product_data, scale=True, product_mass=product_mass)

        self.energy_data_text.setText(energy_data_str)

    @Slot()
    def product_add_clicked(self):
        """ Slot for adding product to the recipe. """
        product = self.product_line_edit.text()
        product_mass = self.product_mass_line_edit.text()

        product_data = self.calories_data.get(product)
        if not product_data or not product_mass.isdigit():
            # Incorrect data, do nothing.
            return

        energy_data = self.scale(
            [product_data["calories"], product_data["protein"], product_data["fat"], product_data["carbohydrates"]],
            scale_factor=product_mass,
        )

        row_count = self.recipe_contents.rowCount()
        self.recipe_contents.insertRow(row_count)
        self.recipe_contents.setItem(row_count, 0, QTableWidgetItem(product))
        self.recipe_contents.setItem(row_count, 1, QTableWidgetItem(product_mass))
        for idx, value in enumerate(energy_data):
            self.recipe_contents.setItem(row_count, 2 + idx, QTableWidgetItem(str(value)))

        total = {"mass": 0, "calories": 0, "protein": 0, "fat": 0, "carbohydrates": 0}
        for row_idx in range(self.recipe_contents.rowCount()):
            product_mass = int(self.recipe_contents.item(row_idx, 1).text())
            total["mass"] += product_mass

            total["calories"] += float(self.recipe_contents.item(row_idx, 2).text())
            total["protein"] += float(self.recipe_contents.item(row_idx, 3).text())
            total["fat"] += float(self.recipe_contents.item(row_idx, 4).text())
            total["carbohydrates"] += float(self.recipe_contents.item(row_idx, 5).text())

        energy_data_str = self.energy_data_str(total, scale=False, product_mass=total["mass"])

        self.recipe_total_info_label.setText(energy_data_str)


def main():
    """ Main application runner. """
    app = QApplication(sys.argv)
    with open(CALORIES_DB_PATH) as file:
        calories_data = json.load(file)
    _app = NutritionApp(calories_data)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
