#!/usr/bin/python
######################################################################
#
# dds.py
#     - Utility for working with DirectDraw Surface file format (.dds)
#     - Support to read files, look at header info.
#     - Generate .dds files
#
# TODO:
#     - Convert data to PNG format and write it out
#
######################################################################

import dds_struct
import os
import logging
from pprint import pprint
from struct import *
import math
import binascii

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

def read_dds(fname):
    """Read a DirectDraw Surface file (.dds)

    Args:
        fname (string): Name of the file to read in.

    Return:
        dds (dds_struct instance): Populated dds_struct, which
            includes header file information and corresponding pixel data.

    Raises:
        ValueError: Raised if we can't find a file to open (i.e. 'fname
            could not be found')
        TypeError: Raised if the header does not look like one of a dds file.
    """

    if not os.path.isfile(fname):
        raise ValueError, "File '%s' could not be found." % fname

    logger.info('Reading file: %s' % fname)
    fhandle = open(fname, 'rb')

    print dds_struct.DDS_HEADER_BEFORE_PIXELFORMAT_SIZE
    
    # Unpack the different components of the header
    dds_header_before_pixelformat = dds_struct.dds_header_before_pixelformat._make(
        unpack(dds_struct.header_before_pixelformat_packed_fmt,
               fhandle.read(dds_struct.DDS_HEADER_BEFORE_PIXELFORMAT_SIZE)))

    pixelformat = dds_struct.pixelformat._make(
        unpack(dds_struct.pixelformat_packed_fmt,
               fhandle.read(dds_struct.PIXELFORMAT_SIZE)))

    dds_header_after_pixelformat = dds_struct.dds_header_after_pixelformat._make(
        unpack(dds_struct.header_after_pixelformat_packed_fmt,
               fhandle.read(dds_struct.DDS_HEADER_AFTER_PIXELFORMAT_SIZE)))

    # Pack the components into a consolidated structure
    dds_header = dds_struct.dds_header._make(list(dds_header_before_pixelformat) \
                                       + [pixelformat] \
                                       + list(dds_header_after_pixelformat))

    # Make sure we're actually working with a .dds file
    # Check the magic number
    # BOZO: This is one of several checks we can do. Add the others (i.e. values of 'size' fields)
    # Put this into some sort of checkDDS() function
    if str(dds_header.dwMagic) != 'DDS ':
        logger.warning("Magic number read: '%s'." % (dds_header.dwMagic))
        raise TypeError, "File '%s' is not a dds file based on header information" % fname

    # If the DDS_PIXELFORMAT dwFlags is set to DDPF_FOURCC and dwFourCC
    # is set to "DX10" an additional DDS_HEADER_DXT10 structure will be present.
    dxt10_header = None
    if int(get_flag_value_in_pixelformat(dds_header.pixelformat, 'dwFlags', 'DDPF_FOURCC')):
        if dds_header.ddspf_dwFourCC == 'DXT10':
            dxt10_header = dds_struct.dxt10_header._make(unpack(dds_struct.dxt10_header_packed_fmt,
                                                                fhandle.read(DXT10_HEADER_SIZE)))
            pass
        pass

    dds_data = fhandle.read()

    dds = dds_struct.dds_struct(header = dds_header,
                                dxt10_header = dxt10_header,
                                data = dds_data)

    logger.info('Done reading file: %s' % fname)

    return dds

def get_flag_value_in_dds_header(dds_header, field_name, flag_name):
    """Get the value of some flag in a field in the dds_header."""

    try:
        field_size = [_field.byte_size for _field in dds_struct.dds_header_fields \
                      if _field.name == field_name][0]
    except IndexError:
        logger.error("Field '%s' does not appear to exist." % field_name)
        raise
    pass

    matching_flag = [flag for flag in dds_struct.dds_flags if flag.name == flag_name][0]
    hex_value = int(getattr(dds_header, field_name).encode('hex'), 16)
    binary_value = bin(hex_value)[2:].zfill(field_size * 8)
    index = int(round(math.log(flag.value, 2)))

    return binary_value[index]

def get_flag_value_in_pixelformat(pixelformat, field_name, flag_name):
    """Get the value of some flag in a field in pixelformat."""

    try:
        field_size = [_field.byte_size for _field in dds_struct.pixelformat_fields \
                      if _field.name == field_name][0]
    except IndexError:
        logger.error("Field '%s' does not appear to exist." % field_name)
        raise

    matching_flag = [flag for flag in dds_struct.pixelformat_flags if flag.name == flag_name][0]
    hex_value = int(getattr(pixelformat, field_name).encode('hex'), 16)
    binary_value = bin(hex_value)[2:].zfill(field_size * 8)
    index = int(round(math.log(flag.value, 2)))

    return binary_value[index]

def get_flag_value_in_dxt10_header(dxt10_header, field_name, flag_name):
    """Get the value of some flag in a field in dxt10_header."""

    try:
        field_size = [_field.byte_size for _field in dds_struct.dxt10_header_fields \
                      if _field.name == field_name][0]
    except IndexError:
        logger.error("Field '%s' does not appear to exist." % field_name)
        raise

    matching_flag = [flag for flag in dds_struct.dxt10_header_flags if flag.name == flag_name][0]
    hex_value = int(getattr(dxt10_header, field_name).encode('hex'), 16)
    binary_value = bin(hex_value)[2:].zfill(field_size * 8)
    index = int(round(math.log(flag.value, 2)))

    return binary_value[index]

def write_dds(fname, dds_header, dds_data, dxt10_header = None):
    """Create a DirectDraw Surface (.dds) file.

    Note: If some non-null dxt10_header value is provided, that will
    be written out regardless of whether the data in dds_header indicates
    it should be exist.

    Args:
        fname (string): Name of the file to create
        dds_header (namedtuple): dds_header info, as defined in dds_struct
        dds_data (array): Raw pixel data
        dxt10_header (namedtuple): dxt10 header info, as defined in dds_struct

    Returns:
        None.

    Raises:
        None.
    """

    # TODO: How do we want to CREATE the header?
    # Original data is immutable, but we may want to create something new from it.

    logger.info('Creating file: %s' % fname)

    fhandle = open(fname, 'wb')

    ########################################################################
    # Write the header up to pixelformat
    for field in dds_struct.dds_header_fields_before_pixelformat:
        field_size_bits = [_field.byte_size for _field in dds_struct.dds_header_fields_before_pixelformat \
                           if _field.name == field.name][0] * 8

        final_val = getattr(dds_header, field.name).encode('hex').zfill(field_size_bits / 4)
        fhandle.write(binascii.unhexlify(final_val))
        pass

    # Then pixelformat
    for field in dds_struct.pixelformat_fields:
        field_size_bits = [_field.byte_size for _field in dds_struct.pixelformat_fields \
                           if _field.name == field.name][0] * 8

        final_val = getattr(dds_header.pixelformat, field.name).encode('hex').zfill(field_size_bits / 4)
        fhandle.write(binascii.unhexlify(final_val))
        pass

    # Then after pixelformat
    for field in dds_struct.dds_header_fields_after_pixelformat:
        field_size_bits = [_field.byte_size for _field in dds_struct.dds_header_fields_after_pixelformat \
                           if _field.name == field.name][0] * 8

        final_val = getattr(dds_header, field.name).encode('hex').zfill(field_size_bits / 4)
        fhandle.write(binascii.unhexlify(final_val))
        pass
    
    ########################################################################
    # If the DXT10_Header was provided, write that out too
    if dxt10_header != None:
        for field in dds_struct.dxt10_header_fields:
            field_size_bits = [_field.byte_size for _field in dds_struct.dxt10_header_fields \
                               if _field.name == field.name][0] * 8

            final_val = getattr(dxt10_header, field.name).encode('hex').zfill(field_size_bits / 4)
            fhandle.write(binascii.unhexlify(final_val))
        pass

    ########################################################################
    # Finally, write out the raw pixel data
    for byte in dds_data:
        # Check to see if we need to unhexlify the data.
        # If it's already a string, then assume it has already
        # been done and just write out the data as-is.
        if type(byte) is str:
            fhandle.write(byte)
        else:
            fhandle.write(binascii.unhexlify(byte))

    fhandle.close()

    logger.info('Done creating file: %s' % fname)
    pass

def print_fields(structure, fields, flags):
    """Pretty print fields listed in 'fields' in structure.

    Generally print each field, the value of that field (with
    corresponding ASCII representation), and then a breakdown
    of any flags in that field, if applicable.
    """

    for field in fields:
        field_size_bits = [_field.byte_size for _field in fields \
                           if _field.name == field.name][0] * 8
        matching_flags = [flag for flag in flags if flag.field_name == field.name]

        # We need to do an endian swap because the struct module does not
        # do any endian swapping for char arrays (which is the format used when reading the file)
        # BOZO: May just be better to stick to using actual ints/doubles to describe
        # the length of the fields to avoid needing this function
        # Update: Tried it -- just opens up another can of worms around correctly interpreting the
        # int values you get back. Doesn't seem worth it atm.
        final_val = int(swap_endian_hex_str(getattr(structure, field.name).encode('hex')), 16)
        bin_val = bin(final_val)[2::]
        padded_bin_val = bin_val.zfill(field_size_bits)
        final_bin_val = padded_bin_val[::-1]

        print field.name, hex(final_val), '(%s)' % final_val, \
            binascii.unhexlify(getattr(structure, field.name).encode('hex'))

        for flag in matching_flags:
            index = int(round(math.log(flag.value, 2)))
            # Flags are binary values, so just print whether value is non-zero.
            try:
                print '\t%s: %d' % (flag.name, int(final_bin_val[index]) > 0)
            except IndexError:
                logger.warning(flag)
                logger.warning(index)
                logger.warning(final_bin_val)
                raise
            pass
        pass
    pass
    
def print_pixelformat(pixelformat):
    """Pretty-print the pixelformat.
    This is mainly for debugging purposes."""

    print '---------------'    
    print 'DDS_PIXELFORMAT'
    print '---------------'
    print_fields(pixelformat, dds_struct.pixelformat_fields, dds_struct.pixelformat_flags)
    pass

def print_dds_header(dds_header):
    """Pretty-print the dds header.

    This is mainly for debugging purposes."""

    print '----------'        
    print 'DDS_HEADER'
    print '----------'    
    print_fields(dds_header, dds_struct.dds_header_fields, dds_struct.dds_header_flags)    
    pass

def print_dxt10_header(dxt10_header):
    """Pretty-print the dds header.

    This is mainly for debugging purposes."""

    print '----------------'    
    print 'DDS_DXT10_HEADER'
    print '----------------'
    if dxt10_header is not None:
        print_fields(dxt10_header, dds_struct.dxt10_header_fields, dds_struct.dxt10_header_flags)
    else:
        print 'Nothing to print.'
    pass

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    DATEFMT ='[%H:%M:%S]'
    FORMAT = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s:%(funcName)s(): %(message)s'

    logging.basicConfig(format=FORMAT,
                        datefmt=DATEFMT,
                        level=logging.DEBUG)
    dds = read_dds('fungus.dds')

    print_dds_header(dds.header)
    print_pixelformat(dds.header.pixelformat)
    print_dxt10_header(dds.dxt10_header)

    write_dds('fungal.dds', dds.header, dds.data)
    pass
