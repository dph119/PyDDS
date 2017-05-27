#!/usr/bin/python
######################################################################
#
# dxt10_header.py
#     - Define a class to contain the dxt10_header data of a
#       DirectDrawSurface (.dds) file.
#
######################################################################

import dds_base
import logging


class dxt10_header(dds_base.dds_base):
    """Reponsible for containing the dxt10_header information in
    a DirectDrawSurface (.dds) file.

    Note: the DXT10 header may not exist in a .dds file"""

    ##############################################################

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.fields = [self.dds_field('dxgiFormat', self.UINT),
                       self.dds_field('resourceDimension', self.UINT),
                       self.dds_field('miscFlag', self.UINT),
                       self.dds_field('arraySize', self.UINT),
                       self.dds_field('miscFlags2', self.UINT)]
    
        self.size = sum([field.byte_size for field in self.fields])
    
        self.flags = [self.dds_flag('miscFlag', 'DDS_RESOURCE_MISC_TEXTURECUBE', 0x4),
                      self.dds_flag('miscFlags2', 'DDS_ALPHA_MODE_UNKNOWN', 0x0),
                      self.dds_flag('miscFlags2', 'DDS_ALPHA_MODE_STRAIGHT', 0x1),
                      self.dds_flag('miscFlags2', 'DDS_ALPHA_MODE_PREMULTIPLIED', 0x2),
                      self.dds_flag('miscFlags2', 'DDS_ALPHA_MODE_OPAQUE', 0x3),
                      self.dds_flag('miscFlags2', 'DDS_ALPHA_MODE_CUSTOM', 0x4)]
    
        self.packed_fmt = ''.join([str(field.byte_size) + 's' \
                                   for field in self.fields])

        self.valid = False
        pass
    
    def print_data(self):
        print '----------------'    
        print 'DDS_DXT10_HEADER'
        print '----------------'
        self.print_fields(self.fields, self.flags)
        pass
    pass
    
