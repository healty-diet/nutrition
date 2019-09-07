""" Tests for the recipe table widget. """

from PySide2.QtWidgets import QTableWidget

from nutrition.recipe_builder_widget.widgets.recipe_table import RecipeTableWidget

from tests.helpers import UsesQApplication, random_string, random_energy_value


class TestRecipeTableWidget(UsesQApplication):
    """ Tests for the recipe name widget. """

    def test_widget_is_qtablewidget(self):
        """ Tests that RecipeTableWidget is inherited from QTableWidget. """
        widget = RecipeTableWidget()

        self.assertTrue(isinstance(widget, QTableWidget))

    def _assert_table_row(self, widget, idx, ingredient_name, energy_value, ingredient_mass):
        self.assertEqual(widget.item(idx, 0).text(), ingredient_name)
        self.assertEqual(widget.item(idx, 1).text(), ingredient_mass)
        self.assertEqual(widget.item(idx, 2).text(), str(energy_value.calories))
        self.assertEqual(widget.item(idx, 3).text(), str(energy_value.protein))
        self.assertEqual(widget.item(idx, 4).text(), str(energy_value.fat))
        self.assertEqual(widget.item(idx, 5).text(), str(energy_value.carbohydrates))

    def test_ingredient_add(self):
        """ Tests the add ingredient method. """
        widget = RecipeTableWidget()

        ingredient_name_0 = random_string()
        energy_value_0 = random_energy_value()
        ingredient_mass_0 = "100"

        ingredient_name_1 = random_string()
        energy_value_1 = random_energy_value()
        ingredient_mass_1 = "100"

        widget.add_ingredient(ingredient_name_0, energy_value_0, ingredient_mass_0)

        self.assertEqual(widget.rowCount(), 1)
        self._assert_table_row(widget, 0, ingredient_name_0, energy_value_0, ingredient_mass_0)

        widget.add_ingredient(ingredient_name_1, energy_value_1, ingredient_mass_1)

        self.assertEqual(widget.rowCount(), 2)
        self._assert_table_row(widget, 0, ingredient_name_0, energy_value_0, ingredient_mass_0)
        self._assert_table_row(widget, 1, ingredient_name_1, energy_value_1, ingredient_mass_1)
