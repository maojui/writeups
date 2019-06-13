
from struct import pack

# http://www.pcschool.com.tw/campus/share/lib/160/
# http://crazycat1130.pixnet.net/blog/post/1345538-%E9%BB%9E%E9%99%A3%E5%9C%96%EF%BC%88bitmap%EF%BC%89%E6%AA%94%E6%A1%88%E6%A0%BC%E5%BC%8F

def add(raw):
    typ         = b'\x42\x4D'               # BM
    size        = pack('<l',len(raw) + 54)  # len(raw) + 54
    reserved1   = b'\x00\x00'
    reserved2   = b'\x00\x00'
    offset      = pack('<l',0x36)           # 36 -> default

    header = typ + size + reserved1 + reserved2 + offset

    size    = pack('<l',40)     # 40 -> default
    width   = pack('<l',1366)   # 1366
    height  = pack('<l',768)
    planes  = b'\x01\x00'
    bits    = b'\x18\x00'
    compression = b'\x00\x00\x00\x00'
    imagesize   = b'\x02\x0C\x30\x00'
    x_resol     = pack('<l',600)
    y_resol     = pack('<l',600)
    ncolours    = b'\x00\x00\x00\x00'
    important_c = b'\x00\x00\x00\x00'
    info_header = size + width + height + planes + bits + compression + imagesize + x_resol + y_resol + ncolours +important_c

    image = header + info_header + raw

    return image

