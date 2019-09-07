""" Tests for the recipe library widget. """
from unittest.mock import patch

from nutrition.recipe import Recipe
from nutrition.recipe_library_widget.widgets.recipe_lookup import RecipeLookupWidget
from nutrition.recipe_library_widget.widgets.recipe_content import RecipeContentWidget
from nutrition.recipe_library_widget import RecipeLibraryWidget

from tests.helpers import UsesQApplication

RECIPE_NAMES = ["test"]
RECIPE = Recipe.from_json(
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


class TestRecipeLibraryWidget(UsesQApplication):
    """ Tests for the recipe library widget. """

    # This is a test, access to the private members is ok.
    # pylint: disable=protected-access

    def assert_children_type(self, widget, expected_type):
        """ Verifies that widget has a child with a given name and this child has expected type. """
        child = widget.findChild(expected_type)
        self.assertIsNotNone(child, "Expected find child with type {}, got None".format(expected_type))
        self.assertTrue(isinstance(child, expected_type))

    @patch("nutrition.recipe.RecipeManager.recipe_names", returns=RECIPE_NAMES, autospec=True)
    def test_recipe_library_layout(self, _mock_recipe_names):
        """ Tests the widget layout. """
        widget = RecipeLibraryWidget()

        expected_children = [RecipeLookupWidget, RecipeContentWidget]

        for child_type in expected_children:
            self.assert_children_type(widget, child_type)

    @patch("nutrition.recipe.RecipeManager.recipe_names", return_value=RECIPE_NAMES, autospec=True)
    def test_recipe_library_init(self, mock_recipe_names):
        """ Tests the widget initialization. """
        widget = RecipeLibraryWidget()

        self.assertTrue(mock_recipe_names.called)
        self.assertEqual(widget._recipe_names, set(RECIPE_NAMES))

    @patch("nutrition.recipe.RecipeManager.recipe_names", return_value=RECIPE_NAMES, autospec=True)
    @patch("nutrition.recipe.RecipeManager.load", return_value=RECIPE, autospec=True)
    def test_recipe_library_lookup(self, _mock_recipe_names, mock_load):
        """ Tests the widget lookup process. """
        widget = RecipeLibraryWidget()

        widget._on_recipe_name_entered(RECIPE_NAMES[0])

        self.assertTrue(mock_load.called)
        self.assertTrue(len(widget._recipe_content_widget.toPlainText()) > 0)
