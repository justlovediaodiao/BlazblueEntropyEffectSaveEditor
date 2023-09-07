import ctypes

class Pref(ctypes.Structure):
    _fields_ = [
        ("unused1", ctypes.c_int * 4),
        ("contentSize", ctypes.c_ulonglong),
        ("unused2", ctypes.c_uint * 2),
        ("compressionLevel", ctypes.c_int),
        ("unused3", ctypes.c_uint * 5)
    ]

def compress(in_name, out_name):
    with open(in_name, 'rb') as fp:
        src = fp.read()

    lib = ctypes.CDLL("./lz4.dll")
    fn = lib.LZ4F_compressFrame
    fn.argtypes = (
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.c_void_p
    )
    fn.restype = ctypes.c_int

    pref = Pref(contentSize=1, compressionLevel=3)
    src_size = len(src)
    dst_size = src_size * 2  # it should be enough
    dst = (ctypes.c_char * dst_size)()
    size = fn(ctypes.byref(dst), dst_size, ctypes.c_char_p(src), src_size, ctypes.byref(pref))
    if size < 0:
        raise OSError(size)

    with open(out_name, 'wb') as fp:
        fp.write(dst[:size])


if __name__ == "__main__":
    def main():
        import sys
        if len(sys.argv) != 3:
            print('Usage: python lz4.py <input> <output>')
            return
        compress(sys.argv[1], sys.argv[2])

    main()
