# FOR STACK TRACE:
# 
#import time
#time.sleep(30)

import six
import sys
import ctypes
import platform

from ctypes.util import find_library

SYSTEM_OS = platform.system()


def zerome(string):
    # find the header size with a dummy string
    dummy = "header finder"
    header = ctypes.string_at(id(dummy), sys.getsizeof(dummy)).find(dummy)

    location = id(string) + header
    size = sys.getsizeof(string) - header
 
    if platform.system() == 'Windows':
        memset = ctypes.cdll.msvcrt.memset
    else:
        libc = find_library('c')
        memset = ctypes.CDLL(libc).memset

    # For OS X, the above should work, but if it doesn't:
    # memset = ctypes.CDLL('libc.dylib').memset
 
    print("Clearing 0x%08x size %i bytes" % (location, size))
 
    memset(location, 0, size)

    #string still with us?
    print(ctypes.string_at(location, size))


def insecure(secret):
    print("Input secret: %s" % secret)

    location = id(secret)
    size = sys.getsizeof(secret)
    
    print("\nMemory location and size of your secret:")
    print(hex(location), size)
 
    # let's try deleting it
    print("\ntrying 'del secret'...")
    del secret

    print("\nMemory reveals:")
    print(ctypes.string_at(location, size))
 
    # maybe we can overwrite it by making a new string?
    print("\nreassigning variable to new string ('blah blah')...")
    secret = "blah blah"

    print("\nMemory reveals:")
    print(ctypes.string_at(location, size))


def trace(frame, event, arg):
    print("%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno))
    return trace


if __name__=='__main__':
    try:
        inp = sys.argv[1] 
    except:
        inp = "super secret"

    insecure(inp)

    print("\nInvoking the nuclear option...")
    #sys.settrace(trace)
    if six.PY3:
        zerome(inp.encode())
    else:
        zerome(inp)


# inspiration from http://web.archive.org/web/20100929111257/http://www.codexon.com/posts/clearing-passwords-in-memory-with-python

