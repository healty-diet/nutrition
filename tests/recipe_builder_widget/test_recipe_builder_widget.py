""" Tests for the recipe builder widget. """
from unittest.mock import patch

from nutrition.recipe_builder_widget import RecipeBuilderWidget
from nutrition.recipe_builder_widget.widgets.recipe_name import RecipeNameWidget
from nutrition.recipe_builder_widget.widgets.serves_amount import ServesAmountWidget
from nutrition.recipe_builder_widget.widgets.ingredient import IngredientWidget
from nutrition.recipe_builder_widget.widgets.energy_value import EnergyValueWidget
from nutrition.recipe_builder_widget.widgets.recipe_table import RecipeTableWidget
from nutrition.recipe_builder_widget.widgets.recipe_text import RecipeTextWidget
from nutrition.recipe_builder_widget.widgets.save_recipe import SaveRecipeWidget
from nutrition.recipe_builder_widget.widgets.total_energy_value import TotalEnergyValueWidget
from nutrition.recipe_builder_widget.widgets.utils import energy_data_str

from tests.helpers import UsesQApplication, random_energy_value

IMPORT_PATH_PREFIX = "nutrition.recipe_builder_widget.widgets"


class TestRecipeBuilderWidget(UsesQApplication):
    """ Tests for the recipe builder widget. """

    # This is a test, access to the private members is ok.
    # pylint: disable=protected-access

    CALORIES_DATA = {"test": random_energy_value()}

    def assert_children_type(self, widget, expected_type):
        """ Verifies that widget has a child with a given name and this child has expected type. """
        child = widget.findChild(expected_type)
        self.assertIsNotNone(child, "Expected find child with type {}, got None".format(expected_type))
        self.assertTrue(isinstance(child, expected_type))

    def test_recipe_builder_layout(self):
        """ Tests the widget layout. """
        widget = RecipeBuilderWidget(self.CALORIES_DATA)

        expected_children = [
            RecipeNameWidget,
            ServesAmountWidget,
            IngredientWidget,
            EnergyValueWidget,
            RecipeTableWidget,
            TotalEnergyValueWidget,
            RecipeTextWidget,
            SaveRecipeWidget,
        ]

        for expected_type in expected_children:
            self.assert_children_type(widget, expected_type)

    def test_recipe_builder_ingredient_entered(self):
        """ Tests that when ingredient entered, the energy value string is updated. """
        widget = RecipeBuilderWidget(self.CALORIES_DATA)

        energy_value_widget = widget.findChild(EnergyValueWidget)

        widget._ingredient_entered("test", 100)

        expected_text = energy_data_str(self.CALORIES_DATA["test"], 100)
        self.assertEqual(energy_value_widget.widget.text(), expected_text)

    def test_recipe_builder_incorrected_ingredient_entered(self):
        """ Tests that when incorrect ingredient entered, nothing happens. """
        widget = RecipeBuilderWidget(self.CALORIES_DATA)

        energy_value_widget = widget.findChild(EnergyValueWidget)

        widget._ingredient_entered("wrong_value", 100)

        expected_text = ""
        self.assertEqual(energy_value_widget.widget.text(), expected_text)

    def test_recipe_builder_ingredient_finalized(self):
        """ Tests that when ingredient finalized, child widgets are updated as expected. """
        widget = RecipeBuilderWidget(self.CALORIES_DATA)

        total_energy_value_widget = widget.findChild(TotalEnergyValueWidget)
        recipe_table_widget = widget.findChild(RecipeTableWidget)

        widget._ingredient_finalized("test", 100)

        expected_text = energy_data_str(self.CALORIES_DATA["test"], None)
        self.assertEqual(total_energy_value_widget.widget.text(), expected_text)
        self.assertEqual(recipe_table_widget.rowCount(), 1)
        self.assertEqual(len(widget._recipe_builder._ingredients), 1)

    @patch("nutrition.recipe.RecipeManager.save", autospec=True)
    @patch(f"{IMPORT_PATH_PREFIX}.recipe_name.RecipeNameWidget.name", return_value="Test", autospec=True)
    @patch(f"{IMPORT_PATH_PREFIX}.recipe_text.RecipeTextWidget.get_text", return_value="Test", autospec=True)
    def test_recipe_builder_save(self, mock_save, _mock_name, _mock_get_text):
        """ Tests _on_save_button_clicked method. """
        widget = RecipeBuilderWidget(self.CALORIES_DATA)

        widget._ingredient_finalized("test", 100)

        widget._on_save_button_clicked()

        self.assertTrue(mock_save.called)
