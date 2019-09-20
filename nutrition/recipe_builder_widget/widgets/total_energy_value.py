""" Module with the Recipe Table Widget. """

from nutrition.utils import InfoWithLabel
from nutrition.recipe.energy_value import EnergyValue
from .utils import energy_data_str


class TotalEnergyValueWidget(InfoWithLabel):
    """ Widget with total energy value for recipe. """

    def __init__(self) -> None:
        super().__init__("Итого (на порцию):", width=300)

    def set_total(self, energy_value: EnergyValue) -> None:
        """ Sets the total energy value. """
        energy_data_per_unit = energy_data_str(energy_value, product_mass=None)
        self.set_text(energy_data_per_unit)
