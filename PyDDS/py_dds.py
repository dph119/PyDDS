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
import binascii
import png
from . import dds_header
from . import dxt10_header
from . import dds_base
from . import block_compression
from . import pixel_swizzle

class PyDDS(dds_base.DDSBase, pixel_swizzle.PixelSwizzle):
    """Reponsible for containing all information of
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

        # TODO: Check the format of this data to see if it even needs
        # to be decompressed. Currently assumes the format is BC1,
        # but obviously won't always be the case

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
        height = int(self.swap_endian_hex_str(self.dds_header.dwHeight.encode('hex')), 16)

        # Check to see if the data contains mipmaps
        # If it does, truncate out everything beyond mip0
        # TODO: Eventually add support to specify which mip level to write out
        mip_map_count = int(self.swap_endian_hex_str(self.dds_header.dwMipMapCount.encode('hex')), 16)

        if mip_map_count > 0:
            # Calculate the size of mip 0 in bytes
            # (number of pixels in mip0) * (bytes/pixel)
            mip0_size = width * height * 4
            data = data[:mip0_size]

        self.logger.info('Creating PNG file: %s (width, height = %d,%d)', fname, width, height)

        fhandle = open(fname, 'wb')
        swizzled_data = self.swizzle_decompressed_bc1_to_png(data, width)
        writer = png.Writer(width, height, alpha=True)

        # PNG expects the data to be presented in "boxed row flat pixel" format:
        # list([R,G,B,A  R,G,B,A  R,G,B,A],
        #      [R,G,B,A  R,G,B,A  R,G,B,A])
        # Each row will be width * # components elements * # bytes/component
        formatted_data = zip(*(iter(swizzled_data),) * (width * 4 * 1))

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
            self.logger.debug("File size (bytes) is: '%d'.", file_size_bytes)
            is_dds = False

        # Check the magic number
        if str(self.dds_header.dwMagic) != 'DDS ':
            self.logger.debug("Magic number read: '%s'.", self.dds_header.dwMagic)
            is_dds = False

        # Check the size of DDS_HEADER
        dds_header_size = int(self.swap_endian_hex_str(self.dds_header.dwSize.encode('hex')), 16)
        if dds_header_size != 124:
            self.logger.debug("DDS_HEADER Size: '%d'.", dds_header_size)
            is_dds = False

        # Check the size of DDS_PIXELFORMAT
        dds_pixelformat_size = int(self.swap_endian_hex_str(self.dds_header.pixelformat.dwSize.encode('hex')), 16)
        if dds_pixelformat_size != 32:
            self.logger.debug("DDS_PIXELFORMAT Size: '%d'.", dds_pixelformat_size)
            is_dds = False

        # Check for a larger minimum filesize if DXT10 format is specified
        if int(self.dds_header.pixelformat.get_flag_value('dwFlags', 'DDPF_FOURCC')):
            if self.dds_header.pixelformat.dwFourCC == 'DXT10':
                if file_size_bytes < 148:
                    self.logger.debug("File size (bytes) with DXT10 header is: '%d'.", file_size_bytes)
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

        # ... and assign the data to is corresponding fields
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

        # Now read the pixel/color data
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
