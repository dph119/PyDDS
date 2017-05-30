#!/usr/bin/python
"""py_dds.py
    - Utility for working with DirectDraw Surface file format (.dds)
    - Support to read files, look at header info.
    - Generate .dds files
    - Rudimentary support to convert data to PNG and write it out.
"""

import sys
sys.dont_write_bytecode = True

import os
import logging
import struct
import png
from . import dds_header
from . import dxt10_header
from . import dds_base
from . import block_compression
from . import pixel_swizzle

class PyDDS(dds_base.DDSBase, pixel_swizzle.PixelSwizzle):
    """Reponsible for managing all DirectDrawSurface (.dds) file data."""

    ##############################################################

    def __init__(self, fname, debug_level=None):
        super(PyDDS, self).__init__(debug_level)
        self.dds_header = dds_header.DDSHeader()
        self.dxt10_header = dxt10_header.DXT10Header()
        self.block_compression = block_compression.BlockCompression()
        self.logger = logging.getLogger(__name__)
        # BOZO: Maybe have a single accessible 'data' attribute, return
        # 'data' vs 'decompressed_data' based on data_is_decompressed flag?
        # TODO: Consider incorporating numpy?
        self.data = []
        self.decompressed_data = []
        self.data_is_decompressed = False

        # Read the file and (if necessary) decompress it
        self.read(fname)
        self.decompress()

    @property
    def format(self):
        """Get the format of the resource."""

        surface_format = self.dds_header.format

        if surface_format == 'DXT10':
            # Real format is actually stored in the DXT10 header
            surface_format = self.dxt10_header.format

        return surface_format

    def decompress(self):
        """If the dds data is compressed (according to the format), go ahead and decompress it,
        storing the results in decompressed_data."""

        if self.format == 'DXGI_FORMAT_BC1_UNORM':
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

        # Check to see if the data contains mipmaps
        # If it does, truncate out everything beyond mip0
        # TODO: Eventually add support to specify which mip level to write out
        if self.dds_header.dwMipMapCount > 0:
            # Calculate the size of mip 0 in bytes
            # (number of pixels in mip0) * (bytes/pixel)
            mip0_size = self.dds_header.dwWidth * self.dds_header.dwHeight * 4
            data = data[:mip0_size]

        self.logger.info('Creating PNG file: %s (width, height = %d,%d)', \
                         fname, self.dds_header.dwWidth, self.dds_header.dwHeight)

        fhandle = open(fname, 'wb')
        swizzled_data = self.swizzle_decompressed_bc1_to_png(data, self.dds_header.dwWidth)

        # TODO: Check if alpha really does exist in original data. Currently assuming it always does.
        writer = png.Writer(self.dds_header.dwWidth, self.dds_header.dwHeight, alpha=True)

        # PNG expects the data to be presented in "boxed row flat pixel" format:
        # list([R,G,B,A  R,G,B,A  R,G,B,A],
        #      [R,G,B,A  R,G,B,A  R,G,B,A])
        # Each row will be width * # components elements * # bytes/component
        formatted_data = zip(*(iter(swizzled_data),) * (self.dds_header.dwWidth * 4 * 1))

        writer.write(fhandle, formatted_data)
        fhandle.close()

        self.logger.info('Done creating PNG file.')

    def print_fields(self):
        self.dds_header.print_fields()
        self.dds_header.pixelformat.print_fields()
        self.dxt10_header.print_fields()

    def check_dds(self, fname):
        """Check the check the data extracted from file to see if this does
        appear to be an actual .dds file."""

        is_dds = True

        # To quote MSDN:
        # To validate a DDS file, a reader should ensure the file
        # is at least 128 bytes long to accommodate the magic value
        # and basic header, the magic value is 0x20534444 ("DDS "),
        # the DDS_HEADER size is 124, and the DDS_PIXELFORMAT in the
        # header size is 32. If the DDS_PIXELFORMAT dwFlags is set to
        # DDPF_FOURCC and a dwFourCC is set to "DX10", then the total
        # file size needs to be at least 148 bytes.

        file_size_bytes = os.path.getsize(fname)
        # Check for minimum file size
        if file_size_bytes < 128:
            self.logger.warning("File size (bytes) is: '%d'.", file_size_bytes)
            is_dds = False

        # Check the magic number
        if self.dds_header.dwMagic != int(self.swap_endian_hex_str('DDS '.encode('hex')), 16):
            self.logger.warning("Magic number read: '%s', but must be %s", self.dds_header.dwMagic,
                                int(self.swap_endian_hex_str('DDS '.encode('hex')), 16))
            is_dds = False

        # Check the size of DDS_HEADER
        if self.dds_header.dwSize != 124:
            self.logger.warning("DDS_HEADER Size: '%d'.", self.dds_header.dwSize)
            is_dds = False

        # Check the size of DDS_PIXELFORMAT
        if self.dds_header.pixelformat.dwSize != 32:
            self.logger.warning("DDS_PIXELFORMAT Size: '%d'.", self.dds_header.pixelformat.dwSize)
            is_dds = False

        # Check for a larger minimum filesize if DXT10 format is specified
        if int(self.dds_header.pixelformat.get_flag_value('dwFlags', 'DDPF_FOURCC')):
            if self.dds_header.pixelformat.dwFourCC == self.swap_endian_hex_str('DXT10'):
                if file_size_bytes < 148:
                    self.logger.warning("File size (bytes) with DXT10 header is: '%d'.", file_size_bytes)
                    is_dds = False

        return is_dds

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

        # Unpack all the data...
        dds_header_before_pixelformat = struct.unpack(self.dds_header.before_pixelformat_packed_fmt,
                                                      fhandle.read(self.dds_header.before_pixelformat_size))

        pixelformat = struct.unpack(self.dds_header.pixelformat.packed_fmt,
                                    fhandle.read(self.dds_header.pixelformat.size))

        dds_header_after_pixelformat = struct.unpack(self.dds_header.after_pixelformat_packed_fmt,
                                                     fhandle.read(self.dds_header.after_pixelformat_size))

        # ... and assign the data to its corresponding fields
        self.dds_header.set_fields(self.dds_header.fields_before_pixelformat, dds_header_before_pixelformat)
        self.dds_header.pixelformat.set_fields(self.dds_header.pixelformat.fields, pixelformat)
        self.dds_header.set_fields(self.dds_header.fields_after_pixelformat, dds_header_after_pixelformat)

        assert self.check_dds(fname), "File '%s' does not appear to be a dds file." % fname

        # If the DDS_PIXELFORMAT dwFlags is set to DDPF_FOURCC and dwFourCC
        # is set to "DX10" an additional DDS_HEADER_DXT10 structure will be present.
        if int(self.dds_header.pixelformat.get_flag_value('dwFlags', 'DDPF_FOURCC')):
            if self.dds_header.pixelformat.dwFourCC == 'DXT10':
                dxt10_header_data = struct.unpack(self.dxt10_header.packed_fmt,
                                                  fhandle.read(self.dxt10_header.size))

                for index, field in enumerate(self.dxt10_header.fields):
                    self.dxt10_header.__dict__[field.name] = dxt10_header_data[index]

        # Now read the pixel/color data, converting to ints
        self.data = [ord(c) for c in fhandle.read()]
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

            final_val = getattr(self.dds_header, field.name)
            fhandle.write(self.convert_to_ascii(final_val, field_size_bits)[::-1])

        # Then pixelformat
        for field in self.dds_header.pixelformat.fields:
            field_size_bits = [_field.byte_size for _field in self.dds_header.pixelformat.fields \
                               if _field.name == field.name][0] * 8

            final_val = getattr(self.dds_header.pixelformat, field.name)
            fhandle.write(self.convert_to_ascii(final_val, field_size_bits)[::-1])

        # Then after pixelformat
        for field in self.dds_header.fields_after_pixelformat:
            field_size_bits = [_field.byte_size for _field in self.dds_header.fields_after_pixelformat \
                               if _field.name == field.name][0] * 8

            final_val = getattr(self.dds_header, field.name)
            fhandle.write(self.convert_to_ascii(final_val, field_size_bits)[::-1])

        ########################################################################
        # If data indicates there is a DXT10_Header was provided, write that out too
        if int(self.dds_header.pixelformat.get_flag_value('dwFlags', 'DDPF_FOURCC')):
            if self.dds_header.pixelformat.dwFourCC == 'DXT10':
                for field in self.dxt10_header.fields:
                    field_size_bits = [_field.byte_size for _field in self.dxt10_header.fields \
                                       if _field.name == field.name][0] * 8

                    final_val = getattr(dxt10_header, field.name)
                    fhandle.write(self.convert_to_ascii(final_val, field_size_bits)[::-1])

        ########################################################################
        # Finally, write out the raw pixel data
        for byte in self.data:
            # Data is internally stored as ints. Convert to ASCII string.
            fhandle.write(self.convert_to_ascii(byte, 8))

        fhandle.close()

        self.logger.info('Done creating file: %s', fname)
