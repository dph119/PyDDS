#!/usr/bin/python
######################################################################
#
# dds_base.py
#     - Define a base class common to all classes that will be used
#       to contain data of a DirectDrawSurface (.dds) file.
#
######################################################################

import abc
from collections import namedtuple
import binascii
import logging
import math
from pprint import pprint


class dds_base(object):
    """Reponsible for containing information common to all classes 
    that will be used to constain data of a DirectDrawSurface (.dds) file."""

    __metaclass__ = abc.ABCMeta
    
    DWORD = 4
    UINT = DWORD

    dds_field = namedtuple('dds_field', 'name byte_size')
    dds_flag = namedtuple('dds_flag', 'field_name name value')

    ##############################################################

    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    @staticmethod
    def swap_endian_hex_str(string):
        """Take some hex string and reverse the byte ordering."""

        # Remove the '0x' prefix if it's there
        if string.startswith('0x'):
            string = string[2:]
            pass
        
        # Note: tried using array module (array.array('h', string)
        # and using byteswap(), but that appears to just swap
        # pairs of bytes, and I really want to reverse the
        # entire ordering

        assert len(string) % 2 == 0, \
            "Provided string (%s) must be an even number of chars" % string

        # Build an array of bytes
        swapped_array = []
        for first, second in zip(string[0::2], string[1::2]):
            hex_char = first + second
            swapped_array.append(hex_char)
            pass
        
        # Swap the elements (bytes) in the array, pack into the string
        swapped_string = ''.join(reversed(swapped_array))

        return swapped_string
    
    def get_flag_value(self, field_name, flag_name):
        """Get the value of some flag in a field."""
        
        try:
            field_size = [_field.byte_size for _field in self.fields \
                          if _field.name == field_name][0]
        except IndexError:
            self.logger.error("Field '%s' does not appear to exist." % field_name)
            raise

        try:
            matching_flag = [flag for flag in self.flags if flag.name == flag_name][0]
        except IndexError:
            self.logger.error("Flag '%s' does not appear to exist." % flag_name)
            raise
        
        hex_value = int(getattr(self, field_name).encode('hex'), 16)
        binary_value = bin(hex_value)[2:].zfill(field_size * 8)
        index = int(round(math.log(flag.value, 2)))

        return binary_value[index]

    def print_fields(self):
        """Pretty print fields listed in 'fields'.

        Generally print each field, the value of that field (with
        corresponding ASCII representation), and then a breakdown
        of any flags in that field, if applicable.
        """

        print '-' * len(self.__name__)
        print self.__name__
        print '-' * len(self.__name__)
        
        for field in self.fields:
            field_size_bits = [_field.byte_size for _field in self.fields \
                               if _field.name == field.name][0] * 8
            matching_flags = [flag for flag in self.flags if flag.field_name == field.name]
            
            # We need to do an endian swap because the struct module does not
            # do any endian swapping for char arrays (which is the format used when reading the file)
            # BOZO: May just be better to stick to using actual ints/doubles to describe
            # the length of the fields to avoid needing this function
            # Update: Tried it -- just opens up another can of worms around correctly interpreting the
            # int values you get back. Doesn't seem worth it atm.
            try:
                final_val = int(self.swap_endian_hex_str(getattr(self, field.name).encode('hex')), 16)
            except AttributeError:
                # If the field does not exist, then just move on to the next one
                continue
            
            bin_val = bin(final_val)[2::]
            padded_bin_val = bin_val.zfill(field_size_bits)
            final_bin_val = padded_bin_val[::-1]

            print field.name, hex(final_val), '(%s)' % final_val, \
                binascii.unhexlify(getattr(self, field.name).encode('hex'))
            
            for flag in matching_flags:
                index = int(round(math.log(flag.value, 2)))
                # Flags are binary values, so just print whether value is non-zero.
                try:
                    print '\t%s: %d' % (flag.name, int(final_bin_val[index]) > 0)
                except IndexError:
                    self.logger.warning(flag)
                    self.logger.warning(index)
                    self.logger.warning(final_bin_val)
                    raise
                pass
            pass
        pass
    pass
