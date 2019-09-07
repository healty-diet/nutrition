""" Energy value data. """
from nutrition.utils import InfoWithLabel
from nutrition.recipe.energy_value import EnergyValue

from .utils import energy_data_str


class EnergyValueWidget(InfoWithLabel):
    """ Widget with energy value of the product. """

    def __init__(self):
        super().__init__("Информация о продукте:", width=300)

    def set_energy_value(self, energy_value: EnergyValue, ingredient_mass: int):
        """ Sets the energy value. """
        energy_data = energy_data_str(energy_value, ingredient_mass, needs_scaling=True)

        self.set_text(energy_data)

