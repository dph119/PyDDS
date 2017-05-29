#!/usr/bin/python
"""
py_dds.py
    - Utility for working with DirectDraw Surface file format (.dds)
    - Support to read files, look at header info.
    - Generate .dds files

TODO:
    - Convert data to PNG format and write it out
"""

import sys
sys.dont_write_bytecode = True

import os
import logging
import struct
import binascii
import png
from . import dds_header
from . import dxt10_header
from . import dds_base
from . import block_compression
from . import pixel_swizzle

class PyDDS(dds_base.DDSBase, pixel_swizzle.PixelSwizzle):
    """Reponsible for containing the pixelformat information in
    a DirectDrawSurface (.dds) file."""

    ##############################################################

    def __init__(self, fname):
        super(PyDDS, self).__init__()
        self.dds_header = dds_header.DDSHeader()
        self.dxt10_header = dxt10_header.DXT10Header()
        self.block_compression = block_compression.BlockCompression()
        self.logger = logging.getLogger(__name__)
        self.data = []
        self.decompressed_data = []
        self.data_is_decompressed = False

        self.read(fname)

    def decompress(self):
        """If the dds data is compressed, go ahead and decompress it,
        storing the results in decompressed_data."""

        self.decompressed_data = self.block_compression.decompress_bc1(self.data)
        self.data_is_decompressed = True

    def write_to_png(self, fname):
        """Write out the pixel data to a .png file."""

        # Figure out which data to write out.
        # If the decompressed data is valid, use that.
        if self.data_is_decompressed:
            data = self.decompressed_data
        else:
            data = self.data

        assert data, 'data must be something valid at this point.'

        height = int(self.swap_endian_hex_str(self.dds_header.dwHeight.encode('hex')), 16)
        width = int(self.swap_endian_hex_str(self.dds_header.dwWidth.encode('hex')), 16)

        self.logger.info('Creating PNG file: %s (width, height = %d,%d)', fname, width, height)

        fhandle = open(fname, 'wb')

        swizzled_data = self.swizzle_decompressed_bc1_to_png(data, width)

        writer = png.Writer(width, height, alpha=True)

        # PNG expects the data to be presented in "boxed row flat pixel" format:
        # list([R,G,B, R,G,B, R,G,B],
        #      [R,G,B, R,G,B, R,G,B])
        # Each row will be width * # components elements * # bytes/component
        formatted_data = zip(*(iter(swizzled_data),) * (width * 4 * 1))

        writer.write(fhandle, formatted_data)
        fhandle.close()

        self.logger.info('Done creating PNG file.')

    def print_fields(self):
        self.dds_header.print_fields()
        self.dds_header.pixelformat.print_fields()
        self.dxt10_header.print_fields()

    def read(self, fname):
        """Read a DirectDraw Surface file (.dds)

        Args:
            fname (string): Name of the file to read in.

        Returns:
            None.

        Raises:
            ValueError: Raised if we can't find a file to open (i.e. 'fname
                could not be found')
            TypeError: Raised if the header does not look like one of a dds file.
        """

        if not os.path.isfile(fname):
            raise ValueError, "File '%s' could not be found." % fname

        self.logger.info('Reading file: %s', fname)
        fhandle = open(fname, 'rb')

        # Unpack the different components of the header
        dds_header_before_pixelformat = struct.unpack(self.dds_header.before_pixelformat_packed_fmt,
                                                      fhandle.read(self.dds_header.before_pixelformat_size))

        for index, field in enumerate(self.dds_header.fields_before_pixelformat):
            self.dds_header.__dict__[field.name] = dds_header_before_pixelformat[index]

        pixelformat = struct.unpack(self.dds_header.pixelformat.packed_fmt,
                                    fhandle.read(self.dds_header.pixelformat.size))

        for index, field in enumerate(self.dds_header.pixelformat.fields):
            self.dds_header.pixelformat.__dict__[field.name] = pixelformat[index]

        dds_header_after_pixelformat = struct.unpack(self.dds_header.after_pixelformat_packed_fmt,
                                                     fhandle.read(self.dds_header.after_pixelformat_size))

        for index, field in enumerate(self.dds_header.fields_after_pixelformat):
            self.dds_header.__dict__[field.name] = dds_header_after_pixelformat[index]

        # Make sure we're actually working with a .dds file
        # Check the magic number
        # BOZO: This is one of several checks we can do. Add the others (i.e. values of 'size' fields)
        # Put this into some sort of checkDDS() function
        if str(self.dds_header.dwMagic) != 'DDS ':
            self.logger.warning("Magic number read: '%s'.", self.dds_header.dwMagic)
            raise TypeError, "File '%s' is not a dds file based on header information" % fname

        # If the DDS_PIXELFORMAT dwFlags is set to DDPF_FOURCC and dwFourCC
        # is set to "DX10" an additional DDS_HEADER_DXT10 structure will be present.
        if int(self.dds_header.pixelformat.get_flag_value('dwFlags', 'DDPF_FOURCC')):
            if self.dds_header.pixelformat.dwFourCC == 'DXT10':
                dxt10_header_data = struct.unpack(self.dxt10_header.packed_fmt,
                                                  fhandle.read(self.dxt10_header.size))

                for index, field in enumerate(self.dxt10_header.fields):
                    self.dxt10_header.__dict__[field.name] = dxt10_header_data[index]

        self.data = fhandle.read()

        self.logger.info('Done reading file: %s', fname)

    def write(self, fname):
        """Create a DirectDraw Surface (.dds) file.

        Args:
            fname (string): Name of the file to read in.

        Returns:
            None.

        Raises:
            None.
        """

        self.logger.info('Creating file: %s', fname)

        fhandle = open(fname, 'wb')

        ########################################################################
        # Write the header up to pixelformat
        for field in self.dds_header.fields_before_pixelformat:
            field_size_bits = [_field.byte_size for _field in self.dds_header.fields_before_pixelformat \
                               if _field.name == field.name][0] * 8

            final_val = getattr(self.dds_header, field.name).encode('hex').zfill(field_size_bits / 4)
            fhandle.write(binascii.unhexlify(final_val))

        # Then pixelformat
        for field in self.dds_header.pixelformat.fields:
            field_size_bits = [_field.byte_size for _field in self.dds_header.pixelformat.fields \
                               if _field.name == field.name][0] * 8

            final_val = getattr(self.dds_header.pixelformat, field.name).encode('hex').zfill(field_size_bits / 4)
            fhandle.write(binascii.unhexlify(final_val))

        # Then after pixelformat
        for field in self.dds_header.fields_after_pixelformat:
            field_size_bits = [_field.byte_size for _field in self.dds_header.fields_after_pixelformat \
                               if _field.name == field.name][0] * 8

            final_val = getattr(self.dds_header, field.name).encode('hex').zfill(field_size_bits / 4)
            fhandle.write(binascii.unhexlify(final_val))

        ########################################################################
        # If data indicates there is a DXT10_Header was provided, write that out too
        if int(self.dds_header.pixelformat.get_flag_value('dwFlags', 'DDPF_FOURCC')):
            if self.dds_header.pixelformat.dwFourCC == 'DXT10':
                for field in self.dxt10_header.fields:
                    field_size_bits = [_field.byte_size for _field in self.dxt10_header.fields \
                                       if _field.name == field.name][0] * 8

                    final_val = getattr(dxt10_header, field.name).encode('hex').zfill(field_size_bits / 4)
                    fhandle.write(binascii.unhexlify(final_val))

        ########################################################################
        # Finally, write out the raw pixel data
        for byte in self.data:
            # Check to see if we need to unhexlify the data.
            # If it's already a string, then assume it has already
            # been done and just write out the data as-is.
            if isinstance(byte, str):
                fhandle.write(byte)
            else:
                fhandle.write(binascii.unhexlify(byte))

        fhandle.close()

        self.logger.info('Done creating file: %s', fname)
