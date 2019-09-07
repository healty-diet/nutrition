""" Tests for the recipe content widget. """

import os

from PySide2.QtWidgets import QPlainTextEdit

from nutrition.recipe_library_widget.widgets.recipe_content import RecipeContentWidget
from nutrition.recipe import Recipe
from nutrition.recipe.types import MeasureName

from tests.helpers import UsesQApplication

TEST_RECIPE = Recipe.from_json(
    """{
  "name": "test",
  "serves_amount": 3,
  "ingredients": [
    {
      "test_ingredient": {
        "gr.": 222
      }
    }
  ],
  "text": "test recipe string",
  "energy_value_per_serving": {
    "calories": 32.56,
    "protein": 0.666,
    "fat": 0.07400000000000001,
    "carbohydrates": 6.66
  }
}"""
)


class TestRecipeContentWidget(UsesQApplication):
    """ Tests for the recipe content widget. """

    def test_recipe_content_is_plaintext(self):
        """ Tests that's widget is derived from QPlainTextEdit. """
        widget = RecipeContentWidget()

        self.assertTrue(isinstance(widget, QPlainTextEdit))

    def test_recipe_recipe_show(self):
        """ Tests the get text method. """
        widget = RecipeContentWidget()

        widget.set_recipe(TEST_RECIPE)

        result_text = widget.toPlainText()
        result_text_lines = list(filter(bool, result_text.split(os.linesep)))

        recipe = TEST_RECIPE
        ingredient = recipe.ingredients[0]
        ingredient_name = list(ingredient.keys())[0]
        ingredient_measure_name = MeasureName(list(ingredient[ingredient_name].keys())[0])
        ingredient_amount = ingredient[ingredient_name][ingredient_measure_name]
        energy_data = recipe.energy_value_per_serving

        expected_lines = [
            "Название: {}".format(recipe.name),
            "Количество порций: {}".format(recipe.serves_amount),
            "Ингредиенты:",
            " - {} ({} {})".format(ingredient_name, ingredient_amount, ingredient_measure_name),
            "Приготовление:",
            recipe.text,
            "Калорийность на порцию: {:.1f} ккал ({:.1f} б, {:.1f} ж, {:.1f} у)".format(
                energy_data.calories, energy_data.protein, energy_data.fat, energy_data.carbohydrates
            ),
        ]

        self.assertEqual(result_text_lines, expected_lines)
