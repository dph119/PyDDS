#!/usr/bin/python
######################################################################
#
# bc.py
#     - Define a class responsible for handling 
#       block-compressed (BC) texture data.
#
######################################################################

from __future__ import division
from pprint import pprint
import logging


class bc(object):
    """Responsible for handling compressed texture data."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)        
        self.R = 0
        self.G = 1
        self.B = 2
        self.A = 3
        self.components = [self.R, self.G, self.B, self.A]
        pass
    
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

        bit_width = {self.R : 5,
                     self.G : 6,
                     self.B : 5}

        component_start = {self.R : 0,
                           self.G : 5,
                           self.B : 10}

        component_end = {self.R : bit_width[self.R] + component_start[self.R],
                         self.G : bit_width[self.G] + component_start[self.G],
                         self.B : bit_width[self.B] + component_start[self.B]}

        decomp_data = []
        for raw_comp_block in zip(*(iter(comp_data),) * 8):
            self.logger.debug('---')
            
            # Convert the raw bytes into actual ints
            comp_block = [ord(c) for c in raw_comp_block]

            self.logger.debug('comp_block:')
            self.logger.debug(comp_block)

            raw_color_0 = ''.join([bin(byte)[2:] for byte in comp_block[0:2]]).zfill(16)
            raw_color_1 = ''.join([bin(byte)[2:] for byte in comp_block[2:4]]).zfill(16)
            
            color_0_val = int(raw_color_0, 2)
            color_1_val = int(raw_color_1, 2)
            
            # Based on how color_0 and color_1 relate to each other, we can be in one of two modes:
            # 1. color_2 and color_3 are linear interpolations between color_0 and color_1
            # 2. color_2 is a linear interpolation between color_0 and color_1, and color_3 is 0
            alpha_exists = color_0_val <= color_1_val

            # Derive the other colors values
            if alpha_exists:
                color_2_val = int((1/2)*color_0_val + (1/2)*color_1_val)
                color_3_val = 0
                pass
            else:
                color_2_val = int((2/3)*color_0_val + (1/3)*color_1_val)
                color_3_val = int((1/3)*color_0_val + (2/3)*color_1_val)
                pass

            raw_color_2 = bin(color_2_val)[2:].zfill(16)
            raw_color_3 = bin(color_3_val)[2:].zfill(16)
            
            color_0 = [None] * 3
            color_1 = [None] * 3
            color_2 = [None] * 3
            color_3 = [None] * 3
            for component in bit_width.keys():
                # Extract the components
                color_0[component] = int(raw_color_0[component_start[component] : component_end[component]], 2)
                color_1[component] = int(raw_color_1[component_start[component] : component_end[component]], 2)
                color_2[component] = int(raw_color_2[component_start[component] : component_end[component]], 2)
                color_3[component] = int(raw_color_3[component_start[component] : component_end[component]], 2)
                pass
                
            colors = [color_0, color_1, color_2, color_3]

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
                    self.logger.warning('index: %d, value: %d' % (index, value))
                    raise
                pass

            if None in decomp_block:
                self.logger.warning('decomp_block:')
                self.logger.warning(decomp_block)
                assert None not in decomp_block, \
                    'All data in decomp_block must be valid at this point'
                pass

            self.logger.debug('decomp_block:')
            self.logger.debug(decomp_block)

            # At this point, the block is organized such that each element
            # is a pixel with 3 components
            # Re-organize this into a simple list of bytes
            # Each component is 1 byte, so just unroll all components of all pixels
            formatted_decomp_block = []
            for pixel in decomp_block:
                for component in pixel:
                    formatted_decomp_block.append(component)

            decomp_data = decomp_data + formatted_decomp_block

            self.logger.debug('formatted_decomp_block:')
            self.logger.debug(formatted_decomp_block)
            pass
        return decomp_data
    pass
        
    

    
