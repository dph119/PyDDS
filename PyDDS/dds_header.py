#!/usr/bin/python
"""dds_header.py
     - Define a class to contain the dds_header data of a
       DirectDrawSurface (.dds) file.
"""

import logging
from . import dds_base
from . import pixelformat



class DDSHeader(dds_base.DDSBase):
    """Reponsible for containing the dds_header information in
    a DirectDrawSurface (.dds) file."""

    ##############################################################

    # pylint: disable=too-many-instance-attributes
    # Can't easily get around the fact we have to split everyting
    # up around pixelformat

    def __init__(self):
        super(DDSHeader, self).__init__()

        self.__name__ = 'DDS_HEADER'
        self.pixelformat = pixelformat.Pixelformat()
        self.logger = logging.getLogger(__name__)

        self.fields_before_pixelformat = [self.dds_field('dwMagic', self.DWORD),
                                          self.dds_field('dwSize', self.DWORD),
                                          self.dds_field('dwFlags', self.DWORD),
                                          self.dds_field('dwHeight', self.DWORD),
                                          self.dds_field('dwWidth', self.DWORD),
                                          self.dds_field('dwPitchOrLinearSize', self.DWORD),
                                          self.dds_field('dwDepth', self.DWORD),
                                          self.dds_field('dwMipMapCount', self.DWORD),
                                          self.dds_field('dwReserved1', self.DWORD * 11)]

        self.fields_after_pixelformat = [self.dds_field('dwCaps', self.DWORD),
                                         self.dds_field('dwCaps2', self.DWORD),
                                         self.dds_field('dwCaps3', self.DWORD),
                                         self.dds_field('dwCaps4', self.DWORD),
                                         self.dds_field('dwReserved2', self.DWORD)]

        self.fields = self.fields_before_pixelformat + self.fields_after_pixelformat

        self.before_pixelformat_size = sum([field.byte_size for field in self.fields_before_pixelformat])
        self.after_pixelformat_size = sum([field.byte_size for field in self.fields_after_pixelformat])
        self.size = self.before_pixelformat_size \
                    + self.pixelformat.size \
                    + self.after_pixelformat_size

        self.flags = [self.dds_flag('dwFlags', 'DDSD_CAPS', 0x1),
                      self.dds_flag('dwFlags', 'DDSD_HEIGHT', 0x2),
                      self.dds_flag('dwFlags', 'DDSD_WIDTH', 0x4),
                      self.dds_flag('dwFlags', 'DDSD_PITCH', 0x8),
                      self.dds_flag('dwFlags', 'DDSD_PIXELFORMAT', 0x1000),
                      self.dds_flag('dwFlags', 'DDSD_MIPMAPCOUNT', 0x20000),
                      self.dds_flag('dwFlags', 'DDSD_LINEARSIZE', 0x80000),
                      self.dds_flag('dwFlags', 'DDSD_DEPTH', 0x800000),
                      self.dds_flag('dwCaps', 'DDSCAPS_COMPLEX', 0x8),
                      self.dds_flag('dwCaps', 'DDSCAPS_MIPMAP', 0x400000),
                      self.dds_flag('dwCaps', 'DDSCAPS_TEXTURE', 0x1000),
                      self.dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP', 0x200),
                      self.dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP_POSITIVEX', 0x400),
                      self.dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP_NEGATIVEX', 0x800),
                      self.dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP_POSITIVEY', 0x1000),
                      self.dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP_NEGATIVEY', 0x2000),
                      self.dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP_POSITIVEZ', 0x4000),
                      self.dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP_NEGATIVEZ', 0x8000),
                      self.dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP_VOLUME', 0x200000)]

        # Describe how the header is packed in the dds file
        self.before_pixelformat_packed_fmt = ''.join([str(field.byte_size) + 's' \
                                                      for field in self.fields_before_pixelformat])

        self.after_pixelformat_packed_fmt = ''.join([str(field.byte_size) + 's' \
                                                     for field in self.fields_after_pixelformat])

        self.packed_fmt = self.before_pixelformat_packed_fmt \
                          + self.pixelformat.packed_fmt \
                          + self.after_pixelformat_packed_fmt
