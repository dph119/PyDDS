"""test_simple.py
    - Define a class of simple unit tests.
"""

import unittest
from PyDDS import PyDDS


class SimpleTest(unittest.TestCase):
    """Define some simple unit tests."""

    def test_read_dds(self):
        """Simply read in a .dds file."""
        self.dds = PyDDS('test/Test.dds')

    def test_decompress_dds(self):
        """Decompress the data read from the .dds file."""
        self.dds = PyDDS('test/Test.dds')
        self.dds.decompress()

    def test_write_dds(self):
        """Write the data out to another .dds file."""
        self.dds = PyDDS('test/Test.dds')
        self.dds.write('test/testy.dds')

    def test_write_dds_to_png(self):
        """Decompress the data from the .dds file, and write to to a .png."""
        self.dds = PyDDS('test/Test.dds')
        self.dds.decompress()
        self.dds.write_to_png('test/dat.png')

if __name__ == '__main__':
    unittest.main()
