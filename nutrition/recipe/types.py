""" Types for recipes. """

from typing import NewType, Dict

MeasureName = NewType("MeasureName", str)

IngredientAmount = NewType("IngredientAmount", Dict[MeasureName, float])

IngredientName = NewType("IngredientName", str)
Ingredient = NewType("Ingredient", Dict[IngredientName, IngredientAmount])


def ingredient(ingredient_name: str, ingredient_measure: str, ingredient_amount: float) -> Ingredient:
    """ Build Ingredient type from provided data. """
    return Ingredient(
        {IngredientName(ingredient_name): IngredientAmount({MeasureName(ingredient_measure): ingredient_amount})}
    )


RecipeName = NewType("RecipeName", str)
