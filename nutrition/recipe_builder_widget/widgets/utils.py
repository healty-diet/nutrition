""" Utils for the recipe module. """
from nutrition.recipe.energy_value import EnergyValue


def scale(energy_value: EnergyValue, scale_factor: float):
    """ Scales energy values for a given mass. """
    modifier = float(scale_factor) / 100.0
    modified_energy_value = EnergyValue()
    for key in energy_value:
        modified_energy_value[key] = energy_value[key] * modifier
    return modified_energy_value


def _energy_data_dict_to_list(product_data):
    """ Makes dict with energy data a list. """
    return [product_data["calories"], product_data["protein"], product_data["fat"], product_data["carbohydrates"]]


def energy_data_str(energy_data: EnergyValue, product_mass=100, needs_scaling=False):
    """ Takes energy data, scales it and returns as a string. """
    if needs_scaling:
        energy_data = scale(energy_data, scale_factor=product_mass)

    data = _energy_data_dict_to_list(energy_data)

    if product_mass:
        return "К {:.1f} Б {:.1f} Ж {:.1f} У {:.1f} [на {} грамм]".format(*data, product_mass)
    else:
        return "К {:.1f} Б {:.1f} Ж {:.1f} У {:.1f}".format(*data)
