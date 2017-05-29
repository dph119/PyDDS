#!/usr/bin/python
"""dds_base.py
    - Define a base class common to all classes that will be used
      to contain data of a DirectDrawSurface (.dds) file.
"""

import abc
from collections import namedtuple
import logging
import math


class DDSBase(object):
    """Reponsible for containing information common to all classes
    that will be used to constain data of a DirectDrawSurface (.dds) file."""

    __metaclass__ = abc.ABCMeta

    DWORD = 4
    UINT = DWORD

    dds_field = namedtuple('dds_field', 'name byte_size')
    dds_flag = namedtuple('dds_flag', 'field_name name value')

    ##############################################################

    def __init__(self):
        # Set up a logger
        logging.basicConfig(format=('%(asctime)s [%(levelname)s]'
                                    '%(filename)s:%(lineno)s:%(funcName)s(): '
                                    '%(message)s'),
                            datefmt='[%H:%M:%S]',
                            level=logging.INFO)

        self.logger = logging.getLogger(__name__)

    @staticmethod
    def convert_to_ascii(value, field_size_bits=None):
        """Given some binary string, convert it into an ASCII string.

        Args:
            value (string or int): Value to convert to ASCII. If it's a string,
                assume it is a binary string.
                If it is an int, it will be internally converted to a binary string.
            field_size_bits (int): Size of value in bits. This is only used if
                we are given an int value and need to convert it to binary.

        Returns:
            ascii_str (string): ASCII representation of value.

        Raises:
            ValueError: If an int is provided, we will need to convert it to a binary
                string and look at field_size_bits, which must be a valid value.
        """

        if isinstance(value, int):
            if field_size_bits is None:
                raise ValueError, ('Need to convert value to a binary string, but a valid '
                                   'value of field_size_bits was not provided.')
            value = bin(value)[2:].zfill(field_size_bits)

        # Work on 8 bits at a time, converting them to an int, and then to an ASCII char.
        # Then concatenate all the chars together into a string.
        return ''.join([chr(int(''.join(byte), 2)) for byte in zip(*(iter(value),) * 8)])

    @staticmethod
    def swap_endian_hex_str(string):
        """Take some hex string and reverse the byte ordering."""

        # Remove the '0x' prefix if it's there
        if string.startswith('0x'):
            string = string[2:]

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

        # Swap the elements (bytes) in the array, pack into the string
        swapped_string = ''.join(reversed(swapped_array))

        return swapped_string

    def get_flag_value(self, field_name, flag_name):
        """Get the value of some flag in a field."""

        try:
            field_size = [_field.byte_size for _field in self.fields \
                          if _field.name == field_name][0]
        except IndexError:
            self.logger.error("Field '%s' does not appear to exist.", field_name)
            raise

        try:
            [flag for flag in self.flags if flag.name == flag_name][0]
        except IndexError:
            self.logger.error("Flag '%s' does not appear to exist.", flag_name)
            raise

        hex_value = getattr(self, field_name)
        binary_value = bin(hex_value)[2:].zfill(field_size * 8)
        index = int(round(math.log(flag.value, 2)))

        return binary_value[index]

    def print_fields(self):
        """Pretty print all the of a DDS file that the class is
        responsible for.

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

            try:
                final_val = getattr(self, field.name)
            except AttributeError:
                # If the field does not exist, then just move on to the next one
                continue

            bin_val = bin(final_val)[2:]
            padded_bin_val = bin_val.zfill(field_size_bits)
            final_bin_val = padded_bin_val[::-1]

            print field.name, hex(final_val), '(%s)' % final_val, \
                self.convert_to_ascii(padded_bin_val, field_size_bits)[::-1]

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

    def set_fields(self, fields, data):
        """Given an array of data and field names, create corresponding attributes
        in the class instance, assigning the corresponding data accordingly.

        Args:
            fields (list of field namedtuples): Fields to set/attributes to create
            data (list of data values to assign to the created fields/attributes

        Returns:
            None.

        Raises:
            None.
        """

        for index, field in enumerate(fields):
            # Convert the data from ASCII representation to int
            self.__dict__[field.name] = int(self.swap_endian_hex_str(data[index].encode('hex')), 16)
