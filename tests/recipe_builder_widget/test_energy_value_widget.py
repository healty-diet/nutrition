""" Tests for the energy value widget. """

from PySide2.QtWidgets import QLabel

from nutrition.recipe_builder_widget.widgets.energy_value import EnergyValueWidget
from nutrition.recipe_builder_widget.widgets.utils import energy_data_str

from tests.helpers import UsesQApplication, random_energy_value


class TestEnergyValueWidget(UsesQApplication):
    """ Tests for the energy value widget. """

    def test_energy_value_has_qlabel(self):
        """ Tests the widget layout. """
        widget = EnergyValueWidget()

        self.assertTrue(hasattr(widget, "widget"))
        self.assertTrue(isinstance(widget.widget, QLabel))

    def test_set_energy_value(self):
        """ Tests the set energy value method. """
        widget = EnergyValueWidget()

        energy_value = random_energy_value()
        ingredient_mass = 100

        widget.set_energy_value(energy_value, ingredient_mass)

        self.assertEqual(widget.widget.text(), energy_data_str(energy_value, ingredient_mass))
