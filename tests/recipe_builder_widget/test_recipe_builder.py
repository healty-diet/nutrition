""" Tests for the recipe builder. """
import unittest

from nutrition.recipe_builder_widget.recipe_builder import RecipeBuilder
from nutrition.recipe_builder_widget.widgets.utils import scale
from nutrition.recipe.types import ingredient as build_ingredient
from nutrition.recipe import Recipe

from tests.helpers import random_energy_value


class TestRecipeBuilder(unittest.TestCase):
    """ Tests for the recipe builder. """

    # This is a test, access to the private members is ok.
    # pylint: disable=protected-access

    def assert_method(self, method_name, field, initial_value, value_to_set):
        """ Checks that provided method works as expected. """

        recipe_builder = RecipeBuilder()
        self.assertEqual(getattr(recipe_builder, field), initial_value)

        method = getattr(recipe_builder, method_name)
        method(value_to_set)

        self.assertEqual(getattr(recipe_builder, field), value_to_set)

    def test_recalculate(self):
        """ Tests recalculate method. """
        recipe_builder = RecipeBuilder()

        ingredient = build_ingredient("test", "g.", 100)
        energy_value = random_energy_value()

        recipe_builder._ingredients = [(ingredient, energy_value)]

        recipe_builder.recalculate()

        self.assertAlmostEqual(energy_value.calories, recipe_builder._energy_value_per_serving.calories)

    def test_add_ingredient(self):
        """ Tests add_ingredient method. """
        recipe_builder = RecipeBuilder()

        ingredient = build_ingredient("test", "g.", 100)
        energy_value = random_energy_value()

        recipe_builder.add_ingredient(ingredient, energy_value)

        self.assertEqual(recipe_builder._ingredients, [(ingredient, energy_value)])

        self.assertAlmostEqual(energy_value.calories, recipe_builder._energy_value_per_serving.calories)

    def test_set_serves_basic(self):
        """ Tests that set_serves method changes amount of serves. """
        self.assert_method("set_serves", "_serves", 1, 3)

    def test_set_serves_changes_energy_value(self):
        """ Tests that after set_serves method energy value is recalculated. """
        recipe_builder = RecipeBuilder()

        ingredient = build_ingredient("test", "g.", 100)
        energy_value = random_energy_value()

        recipe_builder.add_ingredient(ingredient, energy_value)

        recipe_builder.set_serves(2)

        # Default is 100.0, for 2 serves it will be 50.0
        energy_value = scale(energy_value, 50.0)

        self.assertAlmostEqual(energy_value.calories, recipe_builder._energy_value_per_serving.calories)

    def test_set_recipe_name(self):
        """ Tests set_recipe_name method. """
        self.assert_method("set_recipe_name", "_recipe_name", None, "Test")

    def test_set_recipe_text(self):
        """ Tests set_recipe_text method. """
        self.assert_method("set_recipe_text", "_text", None, "Test")

    def test_energy_value(self):
        """ Tests energy_value method. """
        recipe_builder = RecipeBuilder()

        energy_value = random_energy_value()

        recipe_builder._energy_value_per_serving = energy_value

        self.assertEqual(energy_value.calories, recipe_builder.energy_value().calories)

    def test_build(self):
        """ Tests build method. """
        ingredient = build_ingredient("test", "g.", 100)
        energy_value = random_energy_value()

        # Nothing is set.
        recipe_builder = RecipeBuilder()

        with self.assertRaises(RuntimeError):
            recipe_builder.build()

        # Ingredients are not set.
        recipe_builder = RecipeBuilder()
        recipe_builder.set_recipe_name("Test")
        recipe_builder.set_recipe_text("Test")

        with self.assertRaises(RuntimeError):
            recipe_builder.build()

        # Recipe name is not set.
        recipe_builder = RecipeBuilder()
        recipe_builder.add_ingredient(ingredient, energy_value)
        recipe_builder.set_recipe_text("Test")

        with self.assertRaises(RuntimeError):
            recipe_builder.build()

        # Everything is set.
        recipe_builder = RecipeBuilder()
        recipe_builder.add_ingredient(ingredient, energy_value)
        recipe_builder.set_recipe_text("Test")
        recipe_builder.set_recipe_name("Test")
        recipe_builder.set_serves(2)

        recipe = recipe_builder.build()

        self.assertTrue(isinstance(recipe, Recipe))
        self.assertEqual(recipe.name, "Test")
        self.assertEqual(recipe.text, "Test")
        self.assertEqual(recipe.serves_amount, 2)
        self.assertEqual(recipe.ingredients, [ingredient])
        self.assertEqual(recipe.energy_value_per_serving, scale(energy_value, 50.0))
