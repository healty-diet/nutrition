""" Useful helpers for the app. """

from typing import Type, Optional, Callable
from enum import Enum
from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout, QBoxLayout, QLayout, QPushButton
from PySide2.QtCore import Slot

CallbackType = Callable[[], None]


class WidgetWithLabel(QWidget):
    """ Widget that contains label and provided widget in QHBoxLayout. """

    class Layout(Enum):
        """ Widget Layout. """

        HORIZONTAL = 0
        VERTICAL = 1

    def __init__(self, label_text: str, widget: Type[QWidget], layout: Optional[QLayout] = None) -> None:
        super().__init__()

        if layout is None:
            layout = self.Layout.HORIZONTAL

        label = QLabel(label_text)

        direction = QBoxLayout.LeftToRight if layout == self.Layout.HORIZONTAL else QBoxLayout.TopToBottom

        data_layout = QBoxLayout(direction)
        data_layout.addWidget(label)
        data_layout.addWidget(widget)
        if layout == self.Layout.HORIZONTAL:
            data_layout.addStretch()

        self.setLayout(data_layout)

        self.widget = widget


class InfoWithLabel(WidgetWithLabel):
    """ Widget that contains label and updatable text. """

    def __init__(self, label_text: str, width: int = None) -> None:
        widget = QLabel("")
        if width is not None:
            widget.setFixedWidth(300)

        super().__init__(label_text, widget)

    def set_text(self, text: str) -> None:
        """ Sets the text of the stored label. """
        self.widget.setText(text)


class SaveButtonWidget(QWidget):
    """
    Widget with the save button.
    """

    def __init__(self, title: str, on_clicked: CallbackType) -> None:
        self._on_clicked = on_clicked

        super().__init__()

        save_button = QPushButton(title)

        # Layout for the save block

        save_layout = QVBoxLayout()
        save_layout.addWidget(save_button)
        save_layout.addStretch()

        self.setLayout(save_layout)

        self._save_button = save_button
        self._connect_slots()

    def _connect_slots(self) -> None:
        # Lint is disabled because pylint doesn't see .connect method
        # pylint: disable=no-member
        self._save_button.clicked.connect(self._save_button_clicked)

    @Slot()
    def _save_button_clicked(self, _checked: bool) -> None:
        self._on_clicked()
