""" Tests for the total energy value widget. """

from PySide2.QtWidgets import QLabel

from nutrition.recipe_builder_widget.widgets.total_energy_value import TotalEnergyValueWidget
from nutrition.recipe_builder_widget.widgets.utils import energy_data_str

from tests.helpers import UsesQApplication, random_energy_value


class TestTotalEnergyValueWidget(UsesQApplication):
    """ Tests for the energy value widget. """

    def test_total_energy_value_has_qlabel(self):
        """ Tests the widget layout. """
        widget = TotalEnergyValueWidget()

        self.assertTrue(hasattr(widget, "widget"))
        self.assertTrue(isinstance(widget.widget, QLabel))

    def test_set_total(self):
        """ Tests the set total method. """
        widget = TotalEnergyValueWidget()

        energy_value = random_energy_value()

        widget.set_total(energy_value)

        self.assertEqual(widget.widget.text(), energy_data_str(energy_value, product_mass=None))
