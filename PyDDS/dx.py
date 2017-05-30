"""dx.py
    - Define a bunch of DirectX enums and mapping functions.
"""

# Described in DDS_PIXELFORMAT
DXGI_FORMAT_BC1_UNORM = "DXT1"
DXGI_FORMAT_BC2_UNORM = "DXT3"
DXGI_FORMAT_BC3_UNORM = "DXT5"
DXGI_FORMAT_BC4_UNORM = "BC4U"
DXGI_FORMAT_BC4_SNOR = "BC4S"
DXGI_FORMAT_BC5_UNOR = "ATI2"
DXGI_FORMAT_BC5_SNOR = "BC5S"
DXGI_FORMAT_R8G8_B8G8_UNORM = "RGBG"
DXGI_FORMAT_G8R8_G8B8_UNORM = "GRGB"
DXGI_FORMAT_R16G16B16A16_UNORM = 36
DXGI_FORMAT_R16G16B16A16_SNORM = 110
DXGI_FORMAT_R16_FLOAT = 111
DXGI_FORMAT_R16G16_FLOAT = 112
DXGI_FORMAT_R16G16B16A16_FLOAT = 113
DXGI_FORMAT_R32_FLOAT = 114
DXGI_FORMAT_R32G32_FLOAT = 115
DXGI_FORMAT_R32G32B32A32_FLOAT = 116
D3DFMT_DXT2 = "DXT2"
D3DFMT_DXT4 = "DXT4"
D3DFMT_UYVY = "UYVY"
D3DFMT_YUY2 = "YUY2"
# pylint: disable=invalid-name
# I mean, this is literally how's it's listed on MSDN
D3DFMT_CxV8U8 = 117
# pylint: enable=invalid-name

# Dummy value I'm adding to explicitly indicate format is in DXT10_HEADER
DXT10 = "DXT10"

DDS_FMT2STR = {DXGI_FORMAT_BC1_UNORM : 'DXGI_FORMAT_BC1_UNORM',
               DXGI_FORMAT_BC2_UNORM : 'DXGI_FORMAT_BC2_UNORM',
               DXGI_FORMAT_BC3_UNORM : 'DXGI_FORMAT_BC3_UNORM',
               DXGI_FORMAT_BC4_UNORM : 'DXGI_FORMAT_BC4_UNORM',
               DXGI_FORMAT_BC4_SNOR : 'DXGI_FORMAT_BC4_SNOR',
               DXGI_FORMAT_BC5_UNOR : 'DXGI_FORMAT_BC5_UNOR',
               DXGI_FORMAT_BC5_SNOR : 'DXGI_FORMAT_BC5_SNOR',
               DXGI_FORMAT_R8G8_B8G8_UNORM : 'DXGI_FORMAT_R8G8_B8G8_UNORM',
               DXGI_FORMAT_G8R8_G8B8_UNORM : 'DXGI_FORMAT_G8R8_G8B8_UNORM',
               DXGI_FORMAT_R16G16B16A16_UNORM : 'DXGI_FORMAT_R16G16B16A16_UNORM',
               DXGI_FORMAT_R16G16B16A16_SNORM : 'DXGI_FORMAT_R16G16B16A16_SNORM',
               DXGI_FORMAT_R16_FLOAT : 'DXGI_FORMAT_R16_FLOAT',
               DXGI_FORMAT_R16G16_FLOAT : 'DXGI_FORMAT_R16G16_FLOAT',
               DXGI_FORMAT_R16G16B16A16_FLOAT : 'DXGI_FORMAT_R16G16B16A16_FLOAT',
               DXGI_FORMAT_R32_FLOAT : 'DXGI_FORMAT_R32_FLOAT',
               DXGI_FORMAT_R32G32_FLOAT : 'DXGI_FORMAT_R32G32_FLOAT',
               DXGI_FORMAT_R32G32B32A32_FLOAT : 'DXGI_FORMAT_R32G32B32A32_FLOAT',
               D3DFMT_DXT2 : 'D3DFMT_DXT2',
               D3DFMT_DXT4 : 'D3DFMT_DXT4',
               D3DFMT_UYVY : 'D3DFMT_UYVY',
               D3DFMT_YUY2 : 'D3DFMT_YUY2',
               D3DFMT_CxV8U8 : 'D3DFMT_CxV8U8',
               DXT10 : 'DXT10'}

# Described in DXT10_HEADER
DXGI_FORMAT_UNKNOWN = 0
DXGI_FORMAT_R32G32B32A32_TYPELESS = 1
DXGI_FORMAT_R32G32B32A32_FLOAT = 2
DXGI_FORMAT_R32G32B32A32_UINT = 3
DXGI_FORMAT_R32G32B32A32_SINT = 4
DXGI_FORMAT_R32G32B32_TYPELESS = 5
DXGI_FORMAT_R32G32B32_FLOAT = 6
DXGI_FORMAT_R32G32B32_UINT = 7
DXGI_FORMAT_R32G32B32_SINT = 8
DXGI_FORMAT_R16G16B16A16_TYPELESS = 9
DXGI_FORMAT_R16G16B16A16_FLOAT = 10
DXGI_FORMAT_R16G16B16A16_UNORM = 11
DXGI_FORMAT_R16G16B16A16_UINT = 12
DXGI_FORMAT_R16G16B16A16_SNORM = 13
DXGI_FORMAT_R16G16B16A16_SINT = 14
DXGI_FORMAT_R32G32_TYPELESS = 15
DXGI_FORMAT_R32G32_FLOAT = 16
DXGI_FORMAT_R32G32_UINT = 17
DXGI_FORMAT_R32G32_SINT = 18
DXGI_FORMAT_R32G8X24_TYPELESS = 19
DXGI_FORMAT_D32_FLOAT_S8X24_UINT = 20
DXGI_FORMAT_R32_FLOAT_X8X24_TYPELESS = 21
DXGI_FORMAT_X32_TYPELESS_G8X24_UINT = 22
DXGI_FORMAT_R10G10B10A2_TYPELESS = 23
DXGI_FORMAT_R10G10B10A2_UNORM = 24
DXGI_FORMAT_R10G10B10A2_UINT = 25
DXGI_FORMAT_R11G11B10_FLOAT = 26
DXGI_FORMAT_R8G8B8A8_TYPELESS = 27
DXGI_FORMAT_R8G8B8A8_UNORM = 28
DXGI_FORMAT_R8G8B8A8_UNORM_SRGB = 29
DXGI_FORMAT_R8G8B8A8_UINT = 30
DXGI_FORMAT_R8G8B8A8_SNORM = 31
DXGI_FORMAT_R8G8B8A8_SINT = 32
DXGI_FORMAT_R16G16_TYPELESS = 33
DXGI_FORMAT_R16G16_FLOAT = 34
DXGI_FORMAT_R16G16_UNORM = 35
DXGI_FORMAT_R16G16_UINT = 36
DXGI_FORMAT_R16G16_SNORM = 37
DXGI_FORMAT_R16G16_SINT = 38
DXGI_FORMAT_R32_TYPELESS = 39
DXGI_FORMAT_D32_FLOAT = 40
DXGI_FORMAT_R32_FLOAT = 41
DXGI_FORMAT_R32_UINT = 42
DXGI_FORMAT_R32_SINT = 43
DXGI_FORMAT_R24G8_TYPELESS = 44
DXGI_FORMAT_D24_UNORM_S8_UINT = 45
DXGI_FORMAT_R24_UNORM_X8_TYPELESS = 46
DXGI_FORMAT_X24_TYPELESS_G8_UINT = 47
DXGI_FORMAT_R8G8_TYPELESS = 48
DXGI_FORMAT_R8G8_UNORM = 49
DXGI_FORMAT_R8G8_UINT = 50
DXGI_FORMAT_R8G8_SNORM = 51
DXGI_FORMAT_R8G8_SINT = 52
DXGI_FORMAT_R16_TYPELESS = 53
DXGI_FORMAT_R16_FLOAT = 54
DXGI_FORMAT_D16_UNORM = 55
DXGI_FORMAT_R16_UNORM = 56
DXGI_FORMAT_R16_UINT = 57
DXGI_FORMAT_R16_SNORM = 58
DXGI_FORMAT_R16_SINT = 59
DXGI_FORMAT_R8_TYPELESS = 60
DXGI_FORMAT_R8_UNORM = 61
DXGI_FORMAT_R8_UINT = 62
DXGI_FORMAT_R8_SNORM = 63
DXGI_FORMAT_R8_SINT = 64
DXGI_FORMAT_A8_UNORM = 65
DXGI_FORMAT_R1_UNORM = 66
DXGI_FORMAT_R9G9B9E5_SHAREDEXP = 67
DXGI_FORMAT_R8G8_B8G8_UNORM = 68
DXGI_FORMAT_G8R8_G8B8_UNORM = 69
DXGI_FORMAT_BC1_TYPELESS = 70
DXGI_FORMAT_BC1_UNORM = 71
DXGI_FORMAT_BC1_UNORM_SRGB = 72
DXGI_FORMAT_BC2_TYPELESS = 73
DXGI_FORMAT_BC2_UNORM = 74
DXGI_FORMAT_BC2_UNORM_SRGB = 75
DXGI_FORMAT_BC3_TYPELESS = 76
DXGI_FORMAT_BC3_UNORM = 77
DXGI_FORMAT_BC3_UNORM_SRGB = 78
DXGI_FORMAT_BC4_TYPELESS = 79
DXGI_FORMAT_BC4_UNORM = 80
DXGI_FORMAT_BC4_SNORM = 81
DXGI_FORMAT_BC5_TYPELESS = 82
DXGI_FORMAT_BC5_UNORM = 83
DXGI_FORMAT_BC5_SNORM = 84
DXGI_FORMAT_B5G6R5_UNORM = 85
DXGI_FORMAT_B5G5R5A1_UNORM = 86
DXGI_FORMAT_B8G8R8A8_UNORM = 87
DXGI_FORMAT_B8G8R8X8_UNORM = 88
DXGI_FORMAT_R10G10B10_XR_BIAS_A2_UNORM = 89
DXGI_FORMAT_B8G8R8A8_TYPELESS = 90
DXGI_FORMAT_B8G8R8A8_UNORM_SRGB = 91
DXGI_FORMAT_B8G8R8X8_TYPELESS = 92
DXGI_FORMAT_B8G8R8X8_UNORM_SRGB = 93
DXGI_FORMAT_BC6H_TYPELESS = 94
DXGI_FORMAT_BC6H_UF16 = 95
DXGI_FORMAT_BC6H_SF16 = 96
DXGI_FORMAT_BC7_TYPELESS = 97
DXGI_FORMAT_BC7_UNORM = 98
DXGI_FORMAT_BC7_UNORM_SRGB = 99
DXGI_FORMAT_AYUV = 100
DXGI_FORMAT_Y410 = 101
DXGI_FORMAT_Y416 = 102
DXGI_FORMAT_NV12 = 103
DXGI_FORMAT_P010 = 104
DXGI_FORMAT_P016 = 105
DXGI_FORMAT_420_OPAQUE = 106
DXGI_FORMAT_YUY2 = 107
DXGI_FORMAT_Y210 = 108
DXGI_FORMAT_Y216 = 109
DXGI_FORMAT_NV11 = 110
DXGI_FORMAT_AI44 = 111
DXGI_FORMAT_IA44 = 112
DXGI_FORMAT_P8 = 113
DXGI_FORMAT_A8P8 = 114
DXGI_FORMAT_B4G4R4A4_UNORM = 115
DXGI_FORMAT_P208 = 130
DXGI_FORMAT_V208 = 131
DXGI_FORMAT_V408 = 132
DXGI_FORMAT_FORCE_UINT = 0xffffffff

DXT10_FMT2STR = {DXGI_FORMAT_UNKNOWN : 'DXGI_FORMAT_UNKNOWN',
                 DXGI_FORMAT_R32G32B32A32_TYPELESS : 'DXGI_FORMAT_R32G32B32A32_TYPELESS',
                 DXGI_FORMAT_R32G32B32A32_FLOAT : 'DXGI_FORMAT_R32G32B32A32_FLOAT',
                 DXGI_FORMAT_R32G32B32A32_UINT : 'DXGI_FORMAT_R32G32B32A32_UINT',
                 DXGI_FORMAT_R32G32B32A32_SINT : 'DXGI_FORMAT_R32G32B32A32_SINT',
                 DXGI_FORMAT_R32G32B32_TYPELESS : 'DXGI_FORMAT_R32G32B32_TYPELESS',
                 DXGI_FORMAT_R32G32B32_FLOAT : 'DXGI_FORMAT_R32G32B32_FLOAT',
                 DXGI_FORMAT_R32G32B32_UINT : 'DXGI_FORMAT_R32G32B32_UINT',
                 DXGI_FORMAT_R32G32B32_SINT : 'DXGI_FORMAT_R32G32B32_SINT',
                 DXGI_FORMAT_R16G16B16A16_TYPELESS : 'DXGI_FORMAT_R16G16B16A16_TYPELESS',
                 DXGI_FORMAT_R16G16B16A16_FLOAT : 'DXGI_FORMAT_R16G16B16A16_FLOAT',
                 DXGI_FORMAT_R16G16B16A16_UNORM : 'DXGI_FORMAT_R16G16B16A16_UNORM',
                 DXGI_FORMAT_R16G16B16A16_UINT : 'DXGI_FORMAT_R16G16B16A16_UINT',
                 DXGI_FORMAT_R16G16B16A16_SNORM : 'DXGI_FORMAT_R16G16B16A16_SNORM',
                 DXGI_FORMAT_R16G16B16A16_SINT : 'DXGI_FORMAT_R16G16B16A16_SINT',
                 DXGI_FORMAT_R32G32_TYPELESS : 'DXGI_FORMAT_R32G32_TYPELESS',
                 DXGI_FORMAT_R32G32_FLOAT : 'DXGI_FORMAT_R32G32_FLOAT',
                 DXGI_FORMAT_R32G32_UINT : 'DXGI_FORMAT_R32G32_UINT',
                 DXGI_FORMAT_R32G32_SINT : 'DXGI_FORMAT_R32G32_SINT',
                 DXGI_FORMAT_R32G8X24_TYPELESS : 'DXGI_FORMAT_R32G8X24_TYPELESS',
                 DXGI_FORMAT_D32_FLOAT_S8X24_UINT : 'DXGI_FORMAT_D32_FLOAT_S8X24_UINT',
                 DXGI_FORMAT_R32_FLOAT_X8X24_TYPELESS : 'DXGI_FORMAT_R32_FLOAT_X8X24_TYPELESS',
                 DXGI_FORMAT_X32_TYPELESS_G8X24_UINT : 'DXGI_FORMAT_X32_TYPELESS_G8X24_UINT',
                 DXGI_FORMAT_R10G10B10A2_TYPELESS : 'DXGI_FORMAT_R10G10B10A2_TYPELESS',
                 DXGI_FORMAT_R10G10B10A2_UNORM : 'DXGI_FORMAT_R10G10B10A2_UNORM',
                 DXGI_FORMAT_R10G10B10A2_UINT : 'DXGI_FORMAT_R10G10B10A2_UINT',
                 DXGI_FORMAT_R11G11B10_FLOAT : 'DXGI_FORMAT_R11G11B10_FLOAT',
                 DXGI_FORMAT_R8G8B8A8_TYPELESS : 'DXGI_FORMAT_R8G8B8A8_TYPELESS',
                 DXGI_FORMAT_R8G8B8A8_UNORM : 'DXGI_FORMAT_R8G8B8A8_UNORM',
                 DXGI_FORMAT_R8G8B8A8_UNORM_SRGB : 'DXGI_FORMAT_R8G8B8A8_UNORM_SRGB',
                 DXGI_FORMAT_R8G8B8A8_UINT : 'DXGI_FORMAT_R8G8B8A8_UINT',
                 DXGI_FORMAT_R8G8B8A8_SNORM : 'DXGI_FORMAT_R8G8B8A8_SNORM',
                 DXGI_FORMAT_R8G8B8A8_SINT : 'DXGI_FORMAT_R8G8B8A8_SINT',
                 DXGI_FORMAT_R16G16_TYPELESS : 'DXGI_FORMAT_R16G16_TYPELESS',
                 DXGI_FORMAT_R16G16_FLOAT : 'DXGI_FORMAT_R16G16_FLOAT',
                 DXGI_FORMAT_R16G16_UNORM : 'DXGI_FORMAT_R16G16_UNORM',
                 DXGI_FORMAT_R16G16_UINT : 'DXGI_FORMAT_R16G16_UINT',
                 DXGI_FORMAT_R16G16_SNORM : 'DXGI_FORMAT_R16G16_SNORM',
                 DXGI_FORMAT_R16G16_SINT : 'DXGI_FORMAT_R16G16_SINT',
                 DXGI_FORMAT_R32_TYPELESS : 'DXGI_FORMAT_R32_TYPELESS',
                 DXGI_FORMAT_D32_FLOAT : 'DXGI_FORMAT_D32_FLOAT',
                 DXGI_FORMAT_R32_FLOAT : 'DXGI_FORMAT_R32_FLOAT',
                 DXGI_FORMAT_R32_UINT : 'DXGI_FORMAT_R32_UINT',
                 DXGI_FORMAT_R32_SINT : 'DXGI_FORMAT_R32_SINT',
                 DXGI_FORMAT_R24G8_TYPELESS : 'DXGI_FORMAT_R24G8_TYPELESS',
                 DXGI_FORMAT_D24_UNORM_S8_UINT : 'DXGI_FORMAT_D24_UNORM_S8_UINT',
                 DXGI_FORMAT_R24_UNORM_X8_TYPELESS : 'DXGI_FORMAT_R24_UNORM_X8_TYPELESS',
                 DXGI_FORMAT_X24_TYPELESS_G8_UINT : 'DXGI_FORMAT_X24_TYPELESS_G8_UINT',
                 DXGI_FORMAT_R8G8_TYPELESS : 'DXGI_FORMAT_R8G8_TYPELESS',
                 DXGI_FORMAT_R8G8_UNORM : 'DXGI_FORMAT_R8G8_UNORM',
                 DXGI_FORMAT_R8G8_UINT : 'DXGI_FORMAT_R8G8_UINT',
                 DXGI_FORMAT_R8G8_SNORM : 'DXGI_FORMAT_R8G8_SNORM',
                 DXGI_FORMAT_R8G8_SINT : 'DXGI_FORMAT_R8G8_SINT',
                 DXGI_FORMAT_R16_TYPELESS : 'DXGI_FORMAT_R16_TYPELESS',
                 DXGI_FORMAT_R16_FLOAT : 'DXGI_FORMAT_R16_FLOAT',
                 DXGI_FORMAT_D16_UNORM : 'DXGI_FORMAT_D16_UNORM',
                 DXGI_FORMAT_R16_UNORM : 'DXGI_FORMAT_R16_UNORM',
                 DXGI_FORMAT_R16_UINT : 'DXGI_FORMAT_R16_UINT',
                 DXGI_FORMAT_R16_SNORM : 'DXGI_FORMAT_R16_SNORM',
                 DXGI_FORMAT_R16_SINT : 'DXGI_FORMAT_R16_SINT',
                 DXGI_FORMAT_R8_TYPELESS : 'DXGI_FORMAT_R8_TYPELESS',
                 DXGI_FORMAT_R8_UNORM : 'DXGI_FORMAT_R8_UNORM',
                 DXGI_FORMAT_R8_UINT : 'DXGI_FORMAT_R8_UINT',
                 DXGI_FORMAT_R8_SNORM : 'DXGI_FORMAT_R8_SNORM',
                 DXGI_FORMAT_R8_SINT : 'DXGI_FORMAT_R8_SINT',
                 DXGI_FORMAT_A8_UNORM : 'DXGI_FORMAT_A8_UNORM',
                 DXGI_FORMAT_R1_UNORM : 'DXGI_FORMAT_R1_UNORM',
                 DXGI_FORMAT_R9G9B9E5_SHAREDEXP : 'DXGI_FORMAT_R9G9B9E5_SHAREDEXP',
                 DXGI_FORMAT_R8G8_B8G8_UNORM : 'DXGI_FORMAT_R8G8_B8G8_UNORM',
                 DXGI_FORMAT_G8R8_G8B8_UNORM : 'DXGI_FORMAT_G8R8_G8B8_UNORM',
                 DXGI_FORMAT_BC1_TYPELESS : 'DXGI_FORMAT_BC1_TYPELESS',
                 DXGI_FORMAT_BC1_UNORM : 'DXGI_FORMAT_BC1_UNORM',
                 DXGI_FORMAT_BC1_UNORM_SRGB : 'DXGI_FORMAT_BC1_UNORM_SRGB',
                 DXGI_FORMAT_BC2_TYPELESS : 'DXGI_FORMAT_BC2_TYPELESS',
                 DXGI_FORMAT_BC2_UNORM : 'DXGI_FORMAT_BC2_UNORM',
                 DXGI_FORMAT_BC2_UNORM_SRGB : 'DXGI_FORMAT_BC2_UNORM_SRGB',
                 DXGI_FORMAT_BC3_TYPELESS : 'DXGI_FORMAT_BC3_TYPELESS',
                 DXGI_FORMAT_BC3_UNORM : 'DXGI_FORMAT_BC3_UNORM',
                 DXGI_FORMAT_BC3_UNORM_SRGB : 'DXGI_FORMAT_BC3_UNORM_SRGB',
                 DXGI_FORMAT_BC4_TYPELESS : 'DXGI_FORMAT_BC4_TYPELESS',
                 DXGI_FORMAT_BC4_UNORM : 'DXGI_FORMAT_BC4_UNORM',
                 DXGI_FORMAT_BC4_SNORM : 'DXGI_FORMAT_BC4_SNORM',
                 DXGI_FORMAT_BC5_TYPELESS : 'DXGI_FORMAT_BC5_TYPELESS',
                 DXGI_FORMAT_BC5_UNORM : 'DXGI_FORMAT_BC5_UNORM',
                 DXGI_FORMAT_BC5_SNORM : 'DXGI_FORMAT_BC5_SNORM',
                 DXGI_FORMAT_B5G6R5_UNORM : 'DXGI_FORMAT_B5G6R5_UNORM',
                 DXGI_FORMAT_B5G5R5A1_UNORM : 'DXGI_FORMAT_B5G5R5A1_UNORM',
                 DXGI_FORMAT_B8G8R8A8_UNORM : 'DXGI_FORMAT_B8G8R8A8_UNORM',
                 DXGI_FORMAT_B8G8R8X8_UNORM : 'DXGI_FORMAT_B8G8R8X8_UNORM',
                 DXGI_FORMAT_R10G10B10_XR_BIAS_A2_UNORM : 'DXGI_FORMAT_R10G10B10_XR_BIAS_A2_UNORM',
                 DXGI_FORMAT_B8G8R8A8_TYPELESS : 'DXGI_FORMAT_B8G8R8A8_TYPELESS',
                 DXGI_FORMAT_B8G8R8A8_UNORM_SRGB : 'DXGI_FORMAT_B8G8R8A8_UNORM_SRGB',
                 DXGI_FORMAT_B8G8R8X8_TYPELESS : 'DXGI_FORMAT_B8G8R8X8_TYPELESS',
                 DXGI_FORMAT_B8G8R8X8_UNORM_SRGB : 'DXGI_FORMAT_B8G8R8X8_UNORM_SRGB',
                 DXGI_FORMAT_BC6H_TYPELESS : 'DXGI_FORMAT_BC6H_TYPELESS',
                 DXGI_FORMAT_BC6H_UF16 : 'DXGI_FORMAT_BC6H_UF16',
                 DXGI_FORMAT_BC6H_SF16 : 'DXGI_FORMAT_BC6H_SF16',
                 DXGI_FORMAT_BC7_TYPELESS : 'DXGI_FORMAT_BC7_TYPELESS',
                 DXGI_FORMAT_BC7_UNORM : 'DXGI_FORMAT_BC7_UNORM',
                 DXGI_FORMAT_BC7_UNORM_SRGB : 'DXGI_FORMAT_BC7_UNORM_SRGB',
                 DXGI_FORMAT_AYUV : 'DXGI_FORMAT_AYUV',
                 DXGI_FORMAT_Y410 : 'DXGI_FORMAT_Y410',
                 DXGI_FORMAT_Y416 : 'DXGI_FORMAT_Y416',
                 DXGI_FORMAT_NV12 : 'DXGI_FORMAT_NV12',
                 DXGI_FORMAT_P010 : 'DXGI_FORMAT_P010',
                 DXGI_FORMAT_P016 : 'DXGI_FORMAT_P016',
                 DXGI_FORMAT_420_OPAQUE : 'DXGI_FORMAT_420_OPAQUE',
                 DXGI_FORMAT_YUY2 : 'DXGI_FORMAT_YUY2',
                 DXGI_FORMAT_Y210 : 'DXGI_FORMAT_Y210',
                 DXGI_FORMAT_Y216 : 'DXGI_FORMAT_Y216',
                 DXGI_FORMAT_NV11 : 'DXGI_FORMAT_NV11',
                 DXGI_FORMAT_AI44 : 'DXGI_FORMAT_AI44',
                 DXGI_FORMAT_IA44 : 'DXGI_FORMAT_IA44',
                 DXGI_FORMAT_P8 : 'DXGI_FORMAT_P8',
                 DXGI_FORMAT_A8P8 : 'DXGI_FORMAT_A8P8',
                 DXGI_FORMAT_B4G4R4A4_UNORM : 'DXGI_FORMAT_B4G4R4A4_UNORM',
                 DXGI_FORMAT_P208 : 'DXGI_FORMAT_P208',
                 DXGI_FORMAT_V208 : 'DXGI_FORMAT_V208',
                 DXGI_FORMAT_V408 : 'DXGI_FORMAT_V408',
                 DXGI_FORMAT_FORCE_UINT : 'DXGI_FORMAT_FORCE_UINT'}
