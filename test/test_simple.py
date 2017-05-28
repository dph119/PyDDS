"""test_simple.py
    - Define a class of simple unit tests.
"""

import unittest
import logging
from PyDDS import PyDDS


class SimpleTest(unittest.TestCase):
    """Define some simple unit tests."""

    def setUp(self):
        # Read some test file.
        self.dds = PyDDS('test/Test.dds')

        # Set up the logger
        logging.basicConfig(format=('%(asctime)s [%(levelname)s]'
                                    '%(filename)s:%(lineno)s:%(funcName)s(): '
                                    '%(message)s'),
                            datefmt='[%H:%M:%S]',
                            level=logging.INFO)

    def test_decompress_dds(self):
        """Decompress the data read from the .dds file."""
        self.dds.decompress()

    def test_write_dds(self):
        """Write the data out to another .dds file."""
        self.dds.write('test/testy.dds')

    def test_write_dds_to_png(self):
        """Decompress the data from the .dds file, and write to to a .png."""
        self.dds.decompress()
        self.dds.write_to_png('test/dat.png')

if __name__ == '__main__':
    unittest.main()
