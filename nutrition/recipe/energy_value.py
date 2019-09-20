""" Energy value class. """
from typing import Dict


class EnergyValue(dict):
    """ Energy value class (which can be treated like a dict. """

    def __init__(self, calories: float = 0, protein: float = 0, fat: float = 0, carbohydrates: float = 0) -> None:
        super().__init__()
        self["calories"] = calories
        self["protein"] = protein
        self["fat"] = fat
        self["carbohydrates"] = carbohydrates

    @property
    def calories(self) -> float:
        """ Amount of the calories. """
        return float(self["calories"])

    @calories.setter
    def calories(self, value: float) -> None:
        self["calories"] = value

    @property
    def protein(self) -> float:
        """ Amount of the protein. """
        return float(self["protein"])

    @protein.setter
    def protein(self, value: float) -> None:
        self["protein"] = value

    @property
    def fat(self) -> float:
        """ Amount of the fat. """
        return float(self["fat"])

    @fat.setter
    def fat(self, value: float) -> None:
        self["fat"] = value

    @property
    def carbohydrates(self) -> float:
        """ Amount of the carbohydrates. """
        return float(self["carbohydrates"])

    @carbohydrates.setter
    def carbohydrates(self, value: float) -> None:
        self["carbohydrates"] = value

    @classmethod
    def from_dict(cls, dict_value: Dict[str, float]) -> "EnergyValue":
        """ Builds energy value object from dict. """
        return cls(dict_value["calories"], dict_value["protein"], dict_value["fat"], dict_value["carbohydrates"])
