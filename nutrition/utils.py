""" Useful helpers for the app. """

from typing import Type
from enum import Enum
from PySide2.QtWidgets import QWidget, QLabel, QBoxLayout


class WidgetWithLabel(QWidget):
    """ Widget that contains label and provided widget in QHBoxLayout. """

    class Layout(Enum):
        """ Widget Layout. """

        HORIZONTAL = 0
        VERTICAL = 1

    def __init__(self, label_text: str, widget: Type[QWidget], layout=None):
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

    def __init__(self, label_text: str, width: int = None):
        widget = QLabel("")
        if width is not None:
            widget.setFixedWidth(300)

        super().__init__(label_text, widget)

    def set_text(self, text: str):
        """ Sets the text of the stored label. """
        self.widget.setText(text)
