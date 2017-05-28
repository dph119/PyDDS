#!/usr/bin/python
"""
pixelformat.py
    - Define a class to contain the pixelformat data of a
      DirectDrawSurface (.dds) file.
"""

import logging
import dds_base


class Pixelformat(dds_base.DDSBase):
    """Reponsible for containing the pixelformat information in
    a DirectDrawSurface (.dds) file."""

    ##############################################################

    def __init__(self):
        super(Pixelformat, self).__init__()
        self.__name__ = 'DDS_PIXELFORMAT'
        self.logger = logging.getLogger(__name__)

        self.fields = [self.dds_field('dwSize', self.DWORD),
                       self.dds_field('dwFlags', self.DWORD),
                       self.dds_field('dwFourCC', self.DWORD),
                       self.dds_field('dwRGBBitCount', self.DWORD),
                       self.dds_field('dwRbitMask', self.DWORD),
                       self.dds_field('dwGbitMask', self.DWORD),
                       self.dds_field('dwBBitMask', self.DWORD),
                       self.dds_field('dwABitMask', self.DWORD)]

        self.size = sum([field.byte_size for field in self.fields])

        self.flags = [self.dds_flag('dwFlags', 'DDPF_ALPHAPIXELS', 0x1),
                      self.dds_flag('dwFlags', 'DDPF_ALPHA', 0x2),
                      self.dds_flag('dwFlags', 'DDPF_FOURCC', 0x4),
                      self.dds_flag('dwFlags', 'DDPF_RGB', 0x40),
                      self.dds_flag('dwFlags', 'DDPF_YUV', 0x200),
                      self.dds_flag('dwFlags', 'DDPF_LUMINANCE', 0x20000)]

        self.packed_fmt = ''.join([str(field.byte_size) + 's' \
                                   for field in self.fields])
