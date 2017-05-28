#!/usr/bin/python
"""
block_compression.py
     - Define a class responsible for handling
       block-compressed (BC) texture data.
"""

from __future__ import division
import logging


class BlockCompression(object):
    """Responsible for handling compressed texture data."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.red = 0
        self.green = 1
        self.blue = 2
        self.alpha = 3
        self.components = [self.red, self.green, self.blue, self.alpha]

    @staticmethod
    def normalize(value, start_bit_width, end_bit_width):
        """Take some value that's represented by some bit-width
        and generate a corresponding value that is normalized over some other bit-width."""
        return (value / 2**start_bit_width) * (2**end_bit_width)

    def get_bc1_colors_from_block(self, comp_block):
        """Derive the reference colors described in a block of compressed BC1 data."""

        bit_width = {self.red : 5,
                     self.green : 6,
                     self.blue : 5}

        component_start = {self.red : 10,
                           self.green : 5,
                           self.blue : 0}

        component_end = {self.red : bit_width[self.red] + component_start[self.red],
                         self.green : bit_width[self.green] + component_start[self.green],
                         self.blue : bit_width[self.blue] + component_start[self.blue]}

        # Add the initial, directly reported values
        raw_colors = [''.join([bin(byte)[2:] for byte in comp_block[0:2]]).zfill(16),
                      ''.join([bin(byte)[2:] for byte in comp_block[2:4]]).zfill(16)]

        color_val = [int(raw_color, 2) for raw_color in raw_colors]

        # Based on how color_0 and color_1 relate to each other, we can be in one of two modes:
        # 1. color_2 and color_3 are linear interpolations between color_0 and color_1
        # 2. color_2 is a linear interpolation between color_0 and color_1, and color_3 is 0
        # Derive the other colors values
        if color_val[0] <= color_val[1]:
            color_val = color_val + [int((1/2)*color_val[0] + (1/2)*color_val[1]),
                                     0]
        else:
            color_val = color_val + [int((2/3)*color_val[0] + (1/3)*color_val[1]),
                                     int((1/3)*color_val[0] + (2/3)*color_val[1])]

        # Add the derived values
        raw_colors = raw_colors + [bin(color_val[2])[2:].zfill(16), \
                                   bin(color_val[3])[2:].zfill(16)]

        colors = [[None] * 3] * 4

        assert len(colors) == len(raw_colors), 'colors and raw_colors must be the same length.'
        assert None not in raw_colors, 'raw_colors must have valid values at this point'

        for component in bit_width.iterkeys():
            for color, raw_color in zip(colors, raw_colors):
                # Extract the components
                try:
                    color[component] = self.normalize(
                        int(raw_color[component_start[component] : component_end[component]], 2),
                        bit_width[component], 8)
                except KeyError:
                    self.logger.warning("raw_color:")
                    self.logger.warning(raw_color)
                    self.logger.warning("color:")
                    self.logger.warning(color)
                    self.logger.warning("component:")
                    self.logger.warning(component)
                    raise

        return colors

    def decompress_bc1(self, comp_data):
        """Decompress BC1 data.

        Args:
            comp_data (list of bytes): Data to be compressed.

        Returns:
            decomp_data (list of bytes): Decompressed data.

        Raises:
            None.
        """

        # BC1 is arguably the simplest compression algorithm.
        #
        # Each compressed block represents a 4x4 region of texels
        # (read: 16 texels).
        #
        # Each block contains, in order:
        # 1. color_0 (2 bytes)
        # 2. color_1 (2 bytes)
        #    Format of this data is 5_6_5 (R, G, B)
        # 3. 16 2-bit indices, labelled a-p, with each index representing
        #    an index to color_[0|1|2|3].
        #    The size of this is 16 entries * 2 bit/entry = 32 bits
        #    or 4 bytes.
        #
        # Total compressed block size is 4 bytes + 2 bytes + 2 bytes = 8 bytes
        # Compare to the uncompressed size of 4Bpp * 16 pixels = 64 bytes
        # BC1 therefore has a 8:1 compression ratio.
        #
        # Note there is a color_2 and color_3, which are calculated
        # via LERP between color_0 and color_1.
        #
        # color_2 = 2/3*color_0 + 1/3*color_1
        # color_3 = 1/3*color_0 + 2/3*color_1

        # So, work on 8 bytes at a time.
        # Each entry in comp_data is 1 byte.
        decomp_data = []
        for raw_comp_block in zip(*(iter(comp_data),) * 8):
            self.logger.debug('---')

            # Convert the raw bytes into actual ints
            comp_block = [ord(c) for c in raw_comp_block]

            self.logger.debug('comp_block:')
            self.logger.debug(comp_block)

            colors = self.get_bc1_colors_from_block(comp_block)

            self.logger.debug('colors:')
            self.logger.debug(colors)

            indices = ''.join([bin(byte)[2:].zfill(8) for byte in comp_block[4:]])

            self.logger.debug('indices:')
            self.logger.debug(indices)

            assert len(indices) == 32, 'There should be 32 bits of indices.'

            decomp_block = [None] * 16

            for index, first_bit in enumerate(indices[::2]):
                value = int(first_bit + indices[index + 1], 2)
                try:
                    decomp_block[index] = colors[value]
                except IndexError:
                    self.logger.warning('index: %s, value: %s', index, value)
                    raise

            if None in decomp_block:
                self.logger.warning('decomp_block:')
                self.logger.warning(decomp_block)
                assert None not in decomp_block, \
                    'All data in decomp_block must be valid at this point'

            self.logger.debug('decomp_block:')
            self.logger.debug(decomp_block)

            # At this point, the block is organized such that each element
            # is a pixel with 3 components
            # Re-organize this into a simple list of bytes
            # Each component is 1 byte, so just unroll all components of all pixels
            formatted_decomp_block = []
            for pixel in decomp_block:
                formatted_decomp_block = formatted_decomp_block + pixel

            decomp_data = decomp_data + formatted_decomp_block

            self.logger.debug('formatted_decomp_block:')
            self.logger.debug(formatted_decomp_block)

        return decomp_data
