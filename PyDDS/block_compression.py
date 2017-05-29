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
        self.alpha = 3
        self.red = 0
        self.green = 1
        self.blue = 2
        self.components = [self.alpha, self.red, self.green, self.blue]

    @staticmethod
    def normalize(value, start_bit_width, end_bit_width):
        """Take some value that's represented by some bit-width
        and generate a corresponding value that is normalized over some other bit-width."""
        return int((value / (2**start_bit_width)) * (2**end_bit_width))

    def get_bc1_colors_from_block(self, comp_block):
        """Derive the reference colors described in a block of compressed BC1 data."""

        bit_width = {self.red : 5,
                     self.green : 6,
                     self.blue : 5}

        component_start = {self.red : 0,
                           self.green : 5,
                           self.blue : 11}

        component_end = {self.red : bit_width[self.red] + component_start[self.red],
                         self.green : bit_width[self.green] + component_start[self.green],
                         self.blue : bit_width[self.blue] + component_start[self.blue]}

        # Add the initial, directly reported values
        # Each color is considerd a 'word'. Be sure to reverse the bytes.
        raw_colors = [''.join([bin(byte)[2:].zfill(8) for byte in comp_block[0:2][::-1]]).zfill(16),
                      ''.join([bin(byte)[2:].zfill(8) for byte in comp_block[2:4][::-1]]).zfill(16)]

        color_val = [int(raw_color, 2) for raw_color in raw_colors]

        colors = []
        for raw_color in raw_colors:
            color = [None] * 4
            color[self.alpha] = 255
            for component in bit_width.iterkeys():
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
            colors.append(color)

        # Based on how color_0 and color_1 relate to each other, we can be in one of two modes:
        # 1. color_2 and color_3 are linear interpolations between color_0 and color_1
        # 2. color_2 is a linear interpolation between color_0 and color_1, and color_3 is 0
        # Derive the other colors values
        color = [None] * 4
        if color_val[0] <= color_val[1]:
            color[self.alpha] = 255
            for component in bit_width.iterkeys():
                color[component] = int((1/2)*colors[0][component] + (1/2)*colors[1][component])
            colors.append(color)
            colors.append([0, 0, 0, 0])
        else:
            color = [None] * 4
            color[self.alpha] = 255
            for component in bit_width.iterkeys():
                color[component] = int((2/3)*colors[0][component] + (1/3)*colors[1][component])
            colors.append(color)

            color = [None] * 4
            color[self.alpha] = 255
            for component in bit_width.iterkeys():
                color[component] = int((1/3)*colors[0][component] + (2/3)*colors[1][component])
            colors.append(color)

        for color in colors:
            assert len(color) == 4, 'Each color must have 4 components at this point.'

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
        #
        # General note on data structures here: Endianness is on a per 'word'
        # basis, and each word is really just whatever datatype is actually
        # used in DX. So, you can have a word of 2-bytes (such as how color_0 and
        # color_1 are described) and need to swap the bytes,
        # or you can have a word of 1-byte of 2-bits (a row of indices to
        # available colors for a given pixel) and need to swap the ordering of the bits.

        # So, work on 8 bytes at a time.
        # Each entry in comp_data is 1 byte.
        decomp_data = []
        for raw_comp_block in zip(*(iter(comp_data),) * 8):
            self.logger.debug('---')

            # Convert the raw bytes into actual ints
            comp_block = [ord(c) for c in raw_comp_block]

            self.logger.debug('comp_block:')
            self.logger.debug(comp_block)

            # Get the reference colors available for this block
            colors = self.get_bc1_colors_from_block(comp_block)

            self.logger.debug('colors:')
            self.logger.debug(colors)

            # Get the indices for this block
            indices = ''.join([bin(byte)[2:].zfill(8) for byte in comp_block[4:]])
            swapped_indices = ''

            # For every byte of indices, swap the ordering of the pairs of bits
            for byte in zip(*(iter(indices),) * 8):
                for bit_pair in reversed(zip(*(iter(byte),) * 2)):
                    swapped_indices = swapped_indices + ''.join(bit_pair)

            indices = swapped_indices
            assert len(indices) == 32, 'There should be 32 bits of indices.'

            decomp_block = [None] * 16
            for index, bit_pair in enumerate(zip(*(iter(indices),) * 2)):
                # Combine the pair of bits and convert into an int.
                # That's our index.
                decomp_block[index] = colors[int(''.join(bit_pair), 2)]

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
