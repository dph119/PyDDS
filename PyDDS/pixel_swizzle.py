#!/usr/bin/python
"""pixel_swizzle.py
    - Support to swizzle (read: re-arrange) pixel data
      into different configurations.
"""

class PixelSwizzle(object):
    """Responsible for handling swizzling of pixel data."""

    # pylint: disable=too-few-public-methods
    # WIP. More to be added later.

    @staticmethod
    def swizzle_decompressed_bc1_to_png(data, width):
        """Given decompressed BC1 texture data,
        re-arrange to a layout compatible with what is expected
        in the .png file format."""

        # A decompressed block of BC1 data represents
        # a 4x4 region of screenspace.
        # Each pixel has 3 components, where each component
        # is 1 byte. So each decompressed block is
        # 16 pixels * 3 components/pixel * 1 byte/component =
        # 48 bytes.
        #
        # When we write the data to a png file, though,
        # it's expecting everything to be divided into
        # "rows", where each row is an actual horizontal
        # line of pixels in screenspace.
        #
        # Given each row/slice currently represents multiple
        # lines in screenspace, we need to re-arrange it such
        # that we iterate through the first row of all the blocks,
        # then the second, etc. based on provided dimensions.
        #
        # -------------------------------------------------
        # | b0r0 | b0r1 | b0r2 | b0r3 | b1r0 | ... | b0rM |
        # -------------------------------------------------
        #
        # to
        #
        # -------------------------------------------------
        # | b0r0 | b1r0 | b2r0 | b3r0 | b4r0 | ... | bNr0 |
        # -------------------------------------------------
        #
        # where bNrM = block N, row M (of that block)

        bytes_per_block = 16 * 4 * 1
        rows_per_block = 4
        blocks_per_row = width / 4
        bytes_per_block_row = bytes_per_block / rows_per_block
        swizzled_data = []
        blocks = [data[i:i+bytes_per_block] for i in xrange(0, len(data), bytes_per_block)]

        # Each row contains data from 'blocks_per_row' blocks.
        # This is the granularity we will be re-arranging everything.
        # For each group of blocks, grab the first row of each block, then
        # the second row, etc.

        for chunk_of_blocks in zip(*(iter(blocks),) * (blocks_per_row)):
            for row_index in xrange(0, rows_per_block):
                row_start = row_index * bytes_per_block_row
                swizzled_data = swizzled_data + [block[row_start:(row_start+bytes_per_block_row)] \
                                                   for block in chunk_of_blocks]

        # Return a flattened list
        return [element for sublist in swizzled_data for element in sublist]
