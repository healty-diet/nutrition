""" Pool widget. """

from typing import Dict, List, Tuple, Callable, Optional
from enum import Enum

from PySide2.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QPushButton, QComboBox
from PySide2.QtCore import Slot

from nutrition.logger import Logger

PlannedCallbackType = Callable[[str, str, int], None]
RemovedCallbackType = Callable[[str], None]


class PoolElementEditorWidget(QWidget):
    """ Class which handles pool elements planning. """

    def __init__(self, meal_name: str, week_days: List[str], meals_amount: int) -> None:
        super().__init__()

        week_day_list_widget = QComboBox()
        week_day_list_widget.addItems(week_days)

        meal_idx_list_widget = QComboBox()
        meal_idx_list_widget.addItems(list(map(str, range(1, meals_amount + 1))))

        add_push_button = QPushButton("+")

        remove_push_button = QPushButton("-")

        # Layout for the widget

        layout = QHBoxLayout()
        layout.addWidget(week_day_list_widget)
        layout.addWidget(meal_idx_list_widget)
        layout.addWidget(add_push_button)
        layout.addWidget(remove_push_button)

        self.setLayout(layout)

        # Init self data

        self._meal_name = meal_name
        self._on_meal_planned: Optional[PlannedCallbackType] = None
        self._on_element_removed: Optional[RemovedCallbackType] = None

        self._week_day_list_widget = week_day_list_widget
        self._meal_idx_list_widget = meal_idx_list_widget
        self._add_push_button = add_push_button
        self._remove_push_button = remove_push_button

    def set_callbacks(self, on_meal_planned: PlannedCallbackType, on_element_removed: RemovedCallbackType) -> None:
        """ Sets callbacks for widget. """
        self._on_meal_planned = on_meal_planned
        self._on_element_removed = on_element_removed

        self._connect_slots()

    def _connect_slots(self) -> None:
        # Lint is disabled because pylint doesn't see .connect method
        # pylint: disable=no-member
        self._add_push_button.clicked.connect(self._add_meal)
        self._remove_push_button.clicked.connect(self._remove_meal)

    @Slot()
    def _add_meal(self, _checked: bool) -> None:
        if self._on_meal_planned is None:
            return
        week_day = self._week_day_list_widget.currentText()
        meal_idx = int(self._meal_idx_list_widget.currentText())
        self._on_meal_planned(self._meal_name, week_day, meal_idx)

    @Slot()
    def _remove_meal(self, _checked: bool) -> None:
        if self._on_element_removed is None:
            return
        self._on_element_removed(self._meal_name)


class PoolWidget(QWidget):
    """ Pool widget. """

    class _Columns(Enum):
        RECIPE = 0
        SERVES = 1
        ADDING = 2

    DEFAULT_SERVES_AMOUNT = 4

    def __init__(self, week_days: List[str], meals_amount: int, on_meal_planned: PlannedCallbackType) -> None:
        super().__init__()

        recipe_label = QLabel("Блюдо:")
        serves_amount_label = QLabel("Порций:")

        # Widget layout
        layout = QGridLayout()
        layout.addWidget(recipe_label, 0, self._Columns.RECIPE.value)
        layout.addWidget(serves_amount_label, 0, self._Columns.SERVES.value)
        layout.addWidget(QWidget(), 0, self._Columns.ADDING.value)

        self.setLayout(layout)

        # Init self data
        self._meals_amount = meals_amount
        self._week_days = week_days
        self._meal_widgets: Dict[str, Tuple[QLabel, QLabel, PoolElementEditorWidget]] = {}
        self._on_meal_planned = on_meal_planned

    def add_meal(self, meal_name: str, serves_amount: int) -> None:
        """ Adds meal to the pool. """
        Logger().get_logger().debug("Adding meal %s with %i serves", meal_name, serves_amount)

        if meal_name in self._meal_widgets:
            widget = self._meal_widgets[meal_name][self._Columns.SERVES.value]
            serves_amount += int(widget.text())
            widget.setText(str(serves_amount))
            return

        row_idx = self.layout().rowCount()

        recipe_label_widget = QLabel(meal_name)
        serves_amount_widget = QLabel(str(serves_amount))
        editor_widget = PoolElementEditorWidget(meal_name, self._week_days, self._meals_amount)
        editor_widget.set_callbacks(self._meal_planned, self._meal_removed)

        self.layout().addWidget(recipe_label_widget, row_idx, self._Columns.RECIPE.value)
        self.layout().addWidget(serves_amount_widget, row_idx, self._Columns.SERVES.value)
        self.layout().addWidget(editor_widget, row_idx, self._Columns.ADDING.value)

        self._meal_widgets[meal_name] = (recipe_label_widget, serves_amount_widget, editor_widget)

    def _meal_planned(self, meal_name: str, day: str, meal_idx: int) -> None:
        Logger().get_logger().debug("Planning element %s on %s:%i", meal_name, day, meal_idx)

        serves_widget = self._meal_widgets[meal_name][self._Columns.SERVES.value]

        serves_amount = int(serves_widget.text()) - 1
        if serves_amount == 0:
            self._meal_removed(meal_name)
        else:
            serves_widget.setText(str(serves_amount))

        self._on_meal_planned(meal_name, day, meal_idx)

    def _meal_removed(self, meal_name: str) -> None:
        Logger().get_logger().debug("Removing element %s from pool", meal_name)
        for column in self._Columns:
            self._meal_widgets[meal_name][column.value].setParent(None)
            self._meal_widgets[meal_name][column.value].deleteLater()
        del self._meal_widgets[meal_name]
