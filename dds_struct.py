#!/usr/bin/python
######################################################################
#
# dds_struct.py
#     - Define a structure to hold DirectDraw Surface (.dds) data
#
######################################################################

from collections import namedtuple
import array

DWORD = 4
UINT = DWORD

dds_field = namedtuple('dds_field', 'name byte_size')
dds_flag = namedtuple('dds_flag', 'field_name name value')

# DDS_PIXELFORMAT
# ---------------
pixelformat_fields = [dds_field('dwSize', DWORD),
                dds_field('dwFlags', DWORD),
                dds_field('dwFourCC', DWORD),
                dds_field('dwRGBBitCount', DWORD),
                dds_field('dwRbitMask', DWORD),
                dds_field('dwGbitMask', DWORD),                
                dds_field('dwBBitMask', DWORD),
                dds_field('dwABitMask',  DWORD)]

# DDS_HEADER_DXT10
# ----------------
# Note: the DXT10 header will not always exist.
dxt10_header_fields = [dds_field('dxt10_dxgiFormat', UINT),
                       dds_field('dxt10_resourceDimension', UINT),
                       dds_field('dxt10_miscFlag', UINT),
                       dds_field('dxt10_arraySize', UINT),
                       dds_field('dxt10_miscFlags2', UINT)]

# DDS_HEADER
# ----------
dds_header_fields_before_pixelformat = [dds_field('dwMagic', DWORD),
                                        dds_field('dwSize', DWORD),
                                        dds_field('dwFlags', DWORD),
                                        dds_field('dwHeight', DWORD),
                                        dds_field('dwWidth', DWORD),
                                        dds_field('dwPitchOrLinearSize', DWORD),
                                        dds_field('dwDepth', DWORD),
                                        dds_field('dwMipMapCount', DWORD),
                                        dds_field('dwReserved1', DWORD * 11)]

dds_header_fields_after_pixelformat = [dds_field('dwCaps', DWORD),
                                       dds_field('dwCaps2', DWORD),
                                       dds_field('dwCaps3', DWORD),
                                       dds_field('dwCaps4', DWORD),
                                       dds_field('dwReserved2', DWORD)]
                                         
dds_header_fields = dds_header_fields_before_pixelformat + dds_header_fields_after_pixelformat

PIXELFORMAT_SIZE = sum([field.byte_size for field in pixelformat_fields])
DXT10_HEADER_SIZE = sum([field.byte_size for field in dxt10_header_fields])
DDS_HEADER_BEFORE_PIXELFORMAT_SIZE = sum([field.byte_size for field in dds_header_fields_before_pixelformat])
DDS_HEADER_AFTER_PIXELFORMAT_SIZE = sum([field.byte_size for field in dds_header_fields_after_pixelformat])
DDS_HEADER_SIZE = DDS_HEADER_BEFORE_PIXELFORMAT_SIZE \
                  + PIXELFORMAT_SIZE \
                  + DDS_HEADER_AFTER_PIXELFORMAT_SIZE

dds_header_flags = [dds_flag('dwFlags', 'DDSD_CAPS', 0x1),
                    dds_flag('dwFlags', 'DDSD_HEIGHT', 0x2),
                    dds_flag('dwFlags', 'DDSD_WIDTH', 0x4),
                    dds_flag('dwFlags', 'DDSD_PITCH', 0x8),
                    dds_flag('dwFlags', 'DDSD_PIXELFORMAT', 0x1000),
                    dds_flag('dwFlags', 'DDSD_MIPMAPCOUNT', 0x20000),
                    dds_flag('dwFlags', 'DDSD_LINEARSIZE', 0x80000),
                    dds_flag('dwFlags', 'DDSD_DEPTH', 0x800000),
                    dds_flag('dwCaps', 'DDSCAPS_COMPLEX', 0x8),
                    dds_flag('dwCaps', 'DDSCAPS_MIPMAP', 0x400000),
                    dds_flag('dwCaps', 'DDSCAPS_TEXTURE', 0x1000),
                    dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP', 0x200),
                    dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP_POSITIVEX', 0x400),
                    dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP_NEGATIVEX', 0x800),
                    dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP_POSITIVEY', 0x1000),             
                    dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP_NEGATIVEY', 0x2000),
                    dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP_POSITIVEZ', 0x4000),
                    dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP_NEGATIVEZ', 0x8000),
                    dds_flag('dwCaps2', 'DDSCAPS2_CUBEMAP_VOLUME', 0x200000)]

pixelformat_flags = [dds_flag('dwFlags', 'DDPF_ALPHAPIXELS', 0x1),
               dds_flag('dwFlags', 'DDPF_ALPHA', 0x2),
               dds_flag('dwFlags', 'DDPF_FOURCC', 0x4),
               dds_flag('dwFlags', 'DDPF_RGB', 0x40),
               dds_flag('dwFlags', 'DDPF_YUV', 0x200),
               dds_flag('dwFlags', 'DDPF_LUMINANCE', 0x20000)]

dxt10_header_flags = [dds_flag('dxt10_miscFlag', 'DDS_RESOURCE_MISC_TEXTURECUBE', 0x4),
                      dds_flag('dxt10_miscFlags2', 'DDS_ALPHA_MODE_UNKNOWN', 0x0),
                      dds_flag('dxt10_miscFlags2', 'DDS_ALPHA_MODE_STRAIGHT', 0x1),
                      dds_flag('dxt10_miscFlags2', 'DDS_ALPHA_MODE_PREMULTIPLIED', 0x2),
                      dds_flag('dxt10_miscFlags2', 'DDS_ALPHA_MODE_OPAQUE', 0x3),
                      dds_flag('dxt10_miscFlags2', 'DDS_ALPHA_MODE_CUSTOM', 0x4)]

# Define the namedtuples
dds_header_before_pixelformat = namedtuple('dds_header_before_pixelformat',
                                           ' '.join(field.name for field in dds_header_fields_before_pixelformat))

pixelformat = namedtuple('pixelformat',
                         ' '.join(field.name for field in pixelformat_fields))

dds_header_after_pixelformat = namedtuple('dds_header_after_pixelformat',
                                          ' '.join(field.name for field in dds_header_fields_after_pixelformat))

# Note pixelformat is a namedtuple defined above. We have a namedtuple inside a namedtuple.
dds_header = namedtuple('dds_header',
                        ' '.join(field.name for field in dds_header_fields_before_pixelformat) \
                        + ' pixelformat ' \
                        + ' '.join(field.name for field in dds_header_fields_after_pixelformat))

dxt10_header = namedtuple('dxt10_header',
                          ' '.join(field.name for field in dxt10_header_fields))

# Define the final structure to contain everything
dds_struct = namedtuple('dds_struct',
                        'header dxt10_header data')

# Describe how the header is packed in the dds file
header_before_pixelformat_packed_fmt = ''.join([str(field.byte_size) + 's' \
                                                for field in dds_header_fields_before_pixelformat])

header_after_pixelformat_packed_fmt = ''.join([str(field.byte_size) + 's' \
                                               for field in dds_header_fields_after_pixelformat])

pixelformat_packed_fmt = ''.join([str(field.byte_size) + 's' \
                                  for field in pixelformat_fields])


# Ignore first char all but the first fmt, which just indicates endianness.
# It's redundant here.
header_packed_fmt = header_before_pixelformat_packed_fmt \
                    + pixelformat_packed_fmt \
                    + header_after_pixelformat_packed_fmt

dxt10_header_packed_fmt = ''.join([str(field.byte_size) + 's' \
                                   for field in dxt10_header_fields])

