""" Energy value class. """


class EnergyValue(dict):
    """ Energy value class (which can be treated like a dict. """

    def __init__(self, calories=0, protein=0, fat=0, carbohydrates=0):
        super().__init__()
        self["calories"] = calories
        self["protein"] = protein
        self["fat"] = fat
        self["carbohydrates"] = carbohydrates

    @property
    def calories(self):
        """ Amount of the calories. """
        return float(self["calories"])

    @calories.setter
    def calories(self, value):
        self["calories"] = value

    @property
    def protein(self):
        """ Amount of the protein. """
        return float(self["protein"])

    @protein.setter
    def protein(self, value):
        self["protein"] = value

    @property
    def fat(self):
        """ Amount of the fat. """
        return float(self["fat"])

    @fat.setter
    def fat(self, value):
        self["fat"] = value

    @property
    def carbohydrates(self):
        """ Amount of the carbohydrates. """
        return float(self["carbohydrates"])

    @carbohydrates.setter
    def carbohydrates(self, value):
        self["carbohydrates"] = value

    @classmethod
    def from_dict(cls, dict_value):
        """ Builds energy value object from dict. """
        return cls(dict_value["calories"], dict_value["protein"], dict_value["fat"], dict_value["carbohydrates"])
