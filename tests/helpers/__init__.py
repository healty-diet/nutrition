"""Helper classes and functions"""

import os
import unittest

from random import randint

from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QApplication

from nutrition.recipe.energy_value import EnergyValue


class UsesQApplication(unittest.TestCase):
    """Helper class to provide QApplication instances"""

    qapplication = True
    _INSTANCE = None

    def setUp(self):
        """Creates the QApplication instance"""

        # Simple way of making instance a singleton
        super(UsesQApplication, self).setUp()
        if UsesQApplication._INSTANCE is None:
            UsesQApplication._INSTANCE = QApplication([])

        self.app = UsesQApplication._INSTANCE

    def tearDown(self):
        """Deletes the reference owned by self"""
        del self.app
        super(UsesQApplication, self).tearDown()


class UsesQCoreApplication(unittest.TestCase):
    """Helper class for test cases that require an QCoreApplication
    Just connect or call self.exit_app_cb. When called, will ask
    self.app to exit.
    """

    _CORE_INSTANCE = None

    def setUp(self):
        """Set up resources"""
        if UsesQCoreApplication._CORE_INSTANCE is None:
            UsesQCoreApplication._CORE_INSTANCE = QCoreApplication([])

        self.app = UsesQCoreApplication._CORE_INSTANCE

    def tearDown(self):
        """Release resources"""
        del self.app

    def exit_app_cb(self):
        """Quits the application"""
        self.app.exit(0)


class Callback(unittest.TestCase):
    """ Callback class. It takes an expected arguments list on the initialization and
        verifies that callback was called with appropriate values. """

    def __init__(self, expected_args=()):
        super().__init__()
        self.expected_args = expected_args
        self.called = False

    def callback(self, *args):
        """ Actual callback method. """
        self.assertEqual(args, self.expected_args)
        self.called = True


def empty_callback(_data):
    """ Sample empty callback. """
    pass


def random_string(size=5):
    """ Generate random string with the given size. """
    return "".join(map(chr, [randint(33, 126) for x in range(size)]))


def random_energy_value():
    """ Generate ranrom energy value. """
    energy_value = EnergyValue()
    energy_value.calories = randint(1, 500)
    energy_value.protein = randint(1, 500)
    energy_value.fat = randint(1, 500)
    energy_value.carbohydrates = randint(1, 500)

    return energy_value
