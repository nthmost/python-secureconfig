from __future__ import print_function

import ctypes, sys, gc

from secureconfig import SecureString, zeromem

def show_mem(ctypes_tuple):
    location = ctypes_tuple[0]
    size = ctypes_tuple[1]
    print('\nMemory reveals:')
    print(ctypes.string_at(location, size))

def test_zeromem(secret, ctypes_tuple):
    print('\nNuking it from orbit with zeromem:')
    zeromem(secret)
    show_mem(ctypes_tuple)

def test_secure_string(secret):
    print('Input secret: %s' % secret)

    location = id(secret._string)
    size = sys.getsizeof(secret._string)

    print('\nMemory location and size of your secret:')
    print(hex(location), size)

    show_mem((location, size))

    # let's try deleting it
    print('\ntrying \'del secret\'...')

    del(secret)

    show_mem((location, size))
    return (location, size)


key = SecureString('boogers')

ret = test_secure_string(key)

# force garbage collection
del(key)
gc.collect()

show_mem(ret)

#test_zeromem(key, ret)

