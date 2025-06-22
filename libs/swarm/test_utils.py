"""Test cases for utils module."""

import unittest
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(__file__))

from utils import dummy_function


class TestUtils(unittest.TestCase):
    """Test cases for utilities."""

    def test_dummy_function(self):
        """Test that the dummy function returns True."""
        self.assertTrue(dummy_function())


if __name__ == "__main__":
    unittest.main()
