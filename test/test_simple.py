"""test_simple.py
    - Define a class of simple unit tests.
"""

import unittest
import logging
import PyDDS


class SimpleTest(unittest.TestCase):
    """Define some simple unit tests."""

    def setUp(self):
        # Read some test file.
        self.dds = PyDDS.PyDDS('test/Test.dds')

        # Set up the logger
        logging.basicConfig(format=('%(asctime)s [%(levelname)s]'
                                    '%(filename)s:%(lineno)s:%(funcName)s(): '
                                    '%(message)s'),
                            datefmt='[%H:%M:%S]',
                            level=logging.INFO)

    def test_swizzle(self):
        """Swizzle some data to png format."""
        faux_data = [i for i in xrange(0, 192)]

        expected_data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, \
                         48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, \
                         12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, \
                         60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, \
                         24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, \
                         72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, \
                         36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, \
                         84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, \
                         96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, \
                         144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, \
                         108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, \
                         156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, \
                         120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, \
                         168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, \
                         132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, \
                         180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191]

        swizzled_data = self.dds.swizzle_decompressed_bc1_to_png(faux_data, 8)
        self.assertEqual(swizzled_data, expected_data)

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
