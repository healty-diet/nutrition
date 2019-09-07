"""Helper classes and functions"""

import os
import unittest

from random import randint

from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QApplication


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


def random_string(size=5):
    """Generate random string with the given size"""
    return "".join(map(chr, [randint(33, 126) for x in range(size)]))
