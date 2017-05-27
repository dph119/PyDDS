#!/usr/bin/python
######################################################################
#
# pyDDS.py
#     - Utility for working with DirectDraw Surface file format (.dds)
#     - Support to read files, look at header info.
#     - Generate .dds files
#
# TODO:
#     - Convert data to PNG format and write it out
#
######################################################################

import os
import logging
from pprint import pprint
from struct import *
import math
import binascii
import dds_header
import dxt10_header
import dds_base


class pyDDS(dds_base.dds_base):
    """Reponsible for containing the pixelformat information in
    a DirectDrawSurface (.dds) file."""
    
    ##############################################################

    def __init__(self, fname):
        self.dds_header = dds_header.dds_header()
        self.dxt10_header = dxt10_header.dxt10_header()
        self.logger = logging.getLogger(__name__)
        self.data = []

        self.read(fname)
        pass

    def print_data(self):
        self.dds_header.print_data()
        self.dds_header.pixelformat.print_data()
        self.dxt10_header.print_data()
        pass
    
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
        
        self.logger.info('Reading file: %s' % fname)
        fhandle = open(fname, 'rb')

        # Unpack the different components of the header
        dds_header_before_pixelformat = unpack(self.dds_header.before_pixelformat_packed_fmt,
                                               fhandle.read(self.dds_header.before_pixelformat_size))

        for index, field in enumerate(self.dds_header.fields_before_pixelformat):
            self.dds_header.__dict__[field.name] = dds_header_before_pixelformat[index]
            pass
        
        pixelformat = unpack(self.dds_header.pixelformat.packed_fmt,
                             fhandle.read(self.dds_header.pixelformat.size))
        
        for index, field in enumerate(self.dds_header.pixelformat.fields):
            self.dds_header.pixelformat.__dict__[field.name] = pixelformat[index]
            pass
        
        dds_header_after_pixelformat = unpack(self.dds_header.after_pixelformat_packed_fmt,
                                              fhandle.read(self.dds_header.after_pixelformat_size))

        for index, field in enumerate(self.dds_header.fields_after_pixelformat):
            self.dds_header.__dict__[field.name] = dds_header_after_pixelformat[index]
            pass

        # Make sure we're actually working with a .dds file
        # Check the magic number
        # BOZO: This is one of several checks we can do. Add the others (i.e. values of 'size' fields)
        # Put this into some sort of checkDDS() function
        if str(self.dds_header.dwMagic) != 'DDS ':
            self.logger.warning("Magic number read: '%s'." % (self.dds_header.dwMagic))
            raise TypeError, "File '%s' is not a dds file based on header information" % fname

        # If the DDS_PIXELFORMAT dwFlags is set to DDPF_FOURCC and dwFourCC
        # is set to "DX10" an additional DDS_HEADER_DXT10 structure will be present.
        if int(self.dds_header.pixelformat.get_flag_value('dwFlags', 'DDPF_FOURCC')):
            if self.dds_header.pixelformat.dwFourCC == 'DXT10':
                dxt10_header = unpack(self.dxt10_header.packed_fmt,
                                      fhandle.read(self.dxt10_header.size))

                for index, field in enumerate(self.dxt10_header.fields):
                    self.dxt10_header.__dict__[field.name] = dxt10_header[index]
                    pass
                pass
            pass

        self.data = fhandle.read()

        self.logger.info('Done reading file: %s' % fname)
        pass
    
    def write(self, fname):
        """Create a DirectDraw Surface (.dds) file.

        Args:
            fname (string): Name of the file to read in.
          
        Returns:
            None.

        Raises:
            None.
        """

        # TODO: How do we want to CREATE the header?
        # Original data is immutable, but we may want to create something new from it.
        
        self.logger.info('Creating file: %s' % fname)
        
        fhandle = open(fname, 'wb')
        
        ########################################################################
        # Write the header up to pixelformat
        for field in self.dds_header.fields_before_pixelformat:
            field_size_bits = [_field.byte_size for _field in self.dds_header.fields_before_pixelformat \
                               if _field.name == field.name][0] * 8

            final_val = getattr(self.dds_header, field.name).encode('hex').zfill(field_size_bits / 4)
            fhandle.write(binascii.unhexlify(final_val))
            pass

        # Then pixelformat
        for field in self.dds_header.pixelformat.fields:
            field_size_bits = [_field.byte_size for _field in self.dds_header.pixelformat.fields \
                               if _field.name == field.name][0] * 8
            
            final_val = getattr(self.dds_header.pixelformat, field.name).encode('hex').zfill(field_size_bits / 4)
            fhandle.write(binascii.unhexlify(final_val))
            pass
        
        # Then after pixelformat
        for field in self.dds_header.fields_after_pixelformat:
            field_size_bits = [_field.byte_size for _field in self.dds_header.fields_after_pixelformat \
                               if _field.name == field.name][0] * 8
            
            final_val = getattr(self.dds_header, field.name).encode('hex').zfill(field_size_bits / 4)
            fhandle.write(binascii.unhexlify(final_val))
            pass
        
        ########################################################################
        # If data indicates there is a DXT10_Header was provided, write that out too
        if int(self.dds_header.pixelformat.get_flag_value('dwFlags', 'DDPF_FOURCC')):
            if self.dds_header.pixelformat.dwFourCC == 'DXT10':
                for field in dds_struct.dxt10_header_fields:
                    field_size_bits = [_field.byte_size for _field in dds_struct.dxt10_header_fields \
                                       if _field.name == field.name][0] * 8
                
                    final_val = getattr(dxt10_header, field.name).encode('hex').zfill(field_size_bits / 4)
                    fhandle.write(binascii.unhexlify(final_val))
                    pass
                pass
            pass
        
        ########################################################################
        # Finally, write out the raw pixel data
        for byte in self.data:
            # Check to see if we need to unhexlify the data.
            # If it's already a string, then assume it has already
            # been done and just write out the data as-is.
            if type(byte) is str:
                fhandle.write(byte)
            else:
                fhandle.write(binascii.unhexlify(byte))
            pass
        
        fhandle.close()

        self.logger.info('Done creating file: %s' % fname)
        pass

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    DATEFMT ='[%H:%M:%S]'
    FORMAT = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s:%(funcName)s(): %(message)s'

    logging.basicConfig(format=FORMAT,
                        datefmt=DATEFMT,
                        level=logging.DEBUG)
    
    dds = pyDDS('fungus.dds')

    dds.print_data()

    dds.write('fungal.dds')
    pass

