"""test_simple.py
    - Define a class of simple unit tests.
"""

import sys
sys.dont_write_bytecode = True

import unittest
import logging
import PyDDS


class TestSimple(unittest.TestCase):
    """Define some simple unit tests."""

    def setUp(self):
        # Read some test file.
        self.test_dds = PyDDS.PyDDS('test/Test.dds', logging.INFO)
        self.fungus_dds = PyDDS.PyDDS('test/fungus.dds', logging.INFO))

    def test_enum_lookup(self):
        """Test for consistency in the enum look-up functions."""
        for enum in PyDDS.dx.DDS_FMT2STR.iterkeys():
            self.assertEqual(enum,
                             PyDDS.dx.DDS_STR2FMT[PyDDS.dx.DDS_FMT2STR[enum]])

        for enum in PyDDS.dx.DXT10_FMT2STR.iterkeys():
            self.assertEqual(enum,
                             PyDDS.dx.DXT10_STR2FMT[PyDDS.dx.DXT10_FMT2STR[enum]])

    def test_print_format(self):
        """Retrieve and print the format of Test.dds."""
        print self.test_dds.format

    def test_print_fields(self):
        """Simply print the header information of Test.dds"""
        self.test_dds.print_fields()

    def test_swizzle(self):
        """Swizzle some data to png format."""
        faux_data = [i for i in xrange(0, 192)]
        expected_data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, \
                         64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, \
                         16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, \
                         80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, \
                         32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, \
                         96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, \
                         48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, \
                         112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127]

        swizzled_data = self.test_dds.swizzle_decompressed_bc1_to_png(faux_data, 8)
        self.assertEqual(swizzled_data, expected_data)

    def test_write_dds(self):
        """Write the data out to another .dds file."""
        self.test_dds.write('test/Test_copy.dds')
        self.fungus_dds.write('test/fungus_copy.dds')

    def test_write_test_dds_to_png(self):
        """Write the Test.dds data to a .png."""
        self.test_dds.write_to_png('test/Test.png')

    def test_write_fungus_dds_to_png(self):
        """Write fungus.dds data (which contains mipmaps) to a .png."""
        self.fungus_dds.write_to_png('test/fungus.png')

if __name__ == '__main__':
    unittest.main()
