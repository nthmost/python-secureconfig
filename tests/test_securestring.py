from __future__ import print_function

import unittest, ctypes, sys, gc

from secureconfig import SecureString, zeromem

def get_from_mem(ctypes_tuple):
    location = ctypes_tuple[0]
    size = ctypes_tuple[1]
    return ctypes.string_at(location, size)

def learn_mem(item):
    location = id(item)
    size = sys.getsizeof(item)
    return (location, size)


class TestSecureString(unittest.TestCase):

    def setUp(self):
        self.secret = SecureString("it's a secret23 to everybody")

    def tearDown(self):
        del(self.secret)
        #gc.collect()

    def test_SecureString_has_str_methods(self):
        secret = SecureString('test')
        str_methods = set(dir(str))        
        ss_methods = set(dir(SecureString))
        assert(str_methods.issubset(str_methods))

    def test_str_methods_still_work(self):
        # not going to test every single one. a smattering will do.
        secret = SecureString("more than just a dream")
        self.assertFalse(secret.isupper())
        self.assertTrue(secret.islower())
        self.assertTrue(secret.startswith('more'))
        assert(secret.find('than') == 5)

    def test_burn_method_zeroes__string(self):
        ss = SecureString("of all the things I've lost, I miss my mind the most")
        ctuple = learn_mem(ss._string)
        ss.burn()
        gc.collect()
        result = get_from_mem(ctuple)
        print(result)
        print(result.find('things')==-1)
        #self.assertFalse(any(c.isalpha() for c in result))
        self.assertTrue(result.find("of all the things I've lost, I miss my mind the most") == -1)

    def test_SecureString_zeroes_on_del(self):
        ss = SecureString("it's a secret23 to everybody")
        ctuple = learn_mem(ss._string)
        del(ss)
        gc.collect()
        result = get_from_mem(ctuple)
        print(result)
        # TODO:
        # assert that ss no longer exists
        # assert that memory location for ss._string contains no remnants of original string
        

if __name__ == '__main__':
    unittest.main()

