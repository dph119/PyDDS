# PyDDS
Python module for working with DirectDraw Surface files (.dds)

Written in Python 2.7.

This was written at a time when I was messing around with a lot of different DDS file formats. Not all of the formats were actually viewable in DDS viewers like [DDSViewer](https://ddsviewer.com/) or [Nvidia's legacy tools](https://developer.nvidia.com/legacy-texture-tools). I found fewer tools that could convert them to something like PNG when I wanted to just get some qualitative idea of what's going on in the image. 

# Features 
- Manipulate DDS File Contents in Python
    - You can programmatically read in a DDS file and get a sort of "bag of bits", manipulate whatever pixels/channels you care about, and write it back out.
- Convert DDS Files to PNG
    - If there are mipmaps, only mipmap 0 gets dumped.
- Support for uncompressed textures
- BC1 Support

# TODO
- [ ] Convert to Python3
- [ ] User guide info
- [ ] Convert PNG to DDS (need to specify what DDS format to use though)
- [ ] Full MipMap support
- [x] BC1 Support
- [ ] BC2 Support
- [ ] BC3 Support
- [ ] BC4 Support
- [ ] BC5 Support
- [ ] BC6 Support
- [ ] BC7 Support
