""" Utils for the recipe module. """


def scale(data_arr, scale_factor):
    """ Scales energy values for a given mass. """
    modifier = float(scale_factor) / 100.0
    return map(lambda el: float(el) * modifier, data_arr)


def _energy_data_dict_to_list(product_data):
    """ Makes dict with energy data a list. """
    return [product_data["calories"], product_data["protein"], product_data["fat"], product_data["carbohydrates"]]


def energy_data_str(energy_data, product_mass=100, needs_scaling=False):
    """ Takes energy data, scales it and returns as a string. """
    data = _energy_data_dict_to_list(energy_data)
    if needs_scaling:
        data = scale(data, scale_factor=product_mass)
    return "К {:.1f} Б {:.1f} Ж {:.1f} У {:.1f} [на {} грамм]".format(*data, product_mass)
