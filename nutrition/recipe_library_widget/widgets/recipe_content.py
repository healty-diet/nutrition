""" Recipe content widget. """

from PySide2.QtWidgets import QPlainTextEdit

from nutrition.recipe import Recipe
from nutrition.recipe.types import MeasureName


class RecipeContentWidget(QPlainTextEdit):
    """ Recipe content widget. """

    def __init__(self):
        super().__init__()

        self.setReadOnly(True)

    def set_recipe(self, recipe: Recipe):
        """ Sets the provided recipe to the TextEdit. """
        recipe_text = ""

        # Set name.
        recipe_text += "Название: {}\n".format(recipe.name)
        recipe_text += "\n"

        # Set serves amount
        recipe_text += "Количество порций: {}\n".format(recipe.serves_amount)
        recipe_text += "\n"

        # Set ingredients
        recipe_text += "Ингредиенты:\n"
        for ingredient in recipe.ingredients:
            # TODO make ingredient a dict-derived class with handy getters.
            ingredient_name = list(ingredient.keys())[0]
            ingredient_measure_name = MeasureName(list(ingredient[ingredient_name].keys())[0])
            ingredient_amount = ingredient[ingredient_name][ingredient_measure_name]
            recipe_text += " - {} ({} {})\n".format(ingredient_name, ingredient_amount, ingredient_measure_name)
        recipe_text += "\n"

        # Set recipe steps:
        recipe_text += "Приготовление:\n"
        recipe_text += recipe.text
        recipe_text += "\n"
        recipe_text += "\n"

        # Set calories data
        energy_data = recipe.energy_value_per_serving
        recipe_text += "Калорийность на порцию: {:.1f} ккал ({:.1f} б, {:.1f} ж, {:.1f} у)\n".format(
            energy_data.calories, energy_data.protein, energy_data.fat, energy_data.carbohydrates
        )

        self.setPlainText(recipe_text)
