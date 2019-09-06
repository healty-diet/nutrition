""" Types for recipes. """

from typing import NewType, Dict

MeasureName = NewType("MeasureName", str)

IngredientAmount = NewType("IngredientAmount", Dict[MeasureName, float])

IngredientName = NewType("IngredientName", str)
Ingredient = NewType("Ingredient", Dict[IngredientName, IngredientAmount])

RecipeName = NewType("RecipeName", str)
