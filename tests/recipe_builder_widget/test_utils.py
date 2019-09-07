""" Tests for the utils module. """
import unittest

from nutrition.recipe_builder_widget.widgets.utils import scale, energy_data_str
from tests.helpers import random_energy_value


def _build_expected_energy_data_str(energy_value, mass):
    if mass:
        format_str = "К {:.1f} Б {:.1f} Ж {:.1f} У {:.1f} [на {} грамм]"
        return format_str.format(
            energy_value.calories, energy_value.protein, energy_value.fat, energy_value.carbohydrates, mass
        )

    format_str = "К {:.1f} Б {:.1f} Ж {:.1f} У {:.1f}"
    return format_str.format(energy_value.calories, energy_value.protein, energy_value.fat, energy_value.carbohydrates)


class TestUtils(unittest.TestCase):
    """ Tests for the utils module. """

    def test_scale(self):
        """ Tests the scale function. """

        energy_value = random_energy_value()
        scale_factor = 250.0

        scaled = scale(energy_value, scale_factor)

        expected_energy_value = energy_value
        expected_energy_value.calories *= scale_factor / 100.0
        expected_energy_value.protein *= scale_factor / 100.0
        expected_energy_value.fat *= scale_factor / 100.0
        expected_energy_value.carbohydrates *= scale_factor / 100.0

        self.assertAlmostEqual(scaled.calories, expected_energy_value.calories)
        self.assertAlmostEqual(scaled.protein, expected_energy_value.protein)
        self.assertAlmostEqual(scaled.fat, expected_energy_value.fat)
        self.assertAlmostEqual(scaled.carbohydrates, expected_energy_value.carbohydrates)

    def test_energy_data_str_basic(self):
        """ Tests the energy_data_str function. """

        energy_value = random_energy_value()

        energy_value_str = energy_data_str(energy_value)

        expected_str = _build_expected_energy_data_str(energy_value, 100)

        self.assertEqual(energy_value_str, expected_str)

    def test_energy_data_str_scale(self):
        """ Tests the energy_data_str function with scale parameter. """

        energy_value = random_energy_value()
        ingredient_mass = 250

        energy_value_str = energy_data_str(energy_value, ingredient_mass, needs_scaling=True)

        energy_value = scale(energy_value, ingredient_mass)

        expected_str = _build_expected_energy_data_str(energy_value, ingredient_mass)

        self.assertEqual(energy_value_str, expected_str)

    def test_energy_data_str_no_mass(self):
        """ Tests the energy_data_str function with no mass parameter. """

        energy_value = random_energy_value()

        energy_value_str = energy_data_str(energy_value, None)

        expected_str = _build_expected_energy_data_str(energy_value, None)

        self.assertEqual(energy_value_str, expected_str)
