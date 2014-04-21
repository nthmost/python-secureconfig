from __future__ import print_function

import unittest, os, json

from cryptography.fernet import InvalidToken

from secureconfig.cryptkeeper import *
from secureconfig import SecureConfig, SecureJson

CWD = os.path.dirname(os.path.realpath(__file__))

# please don't use any of these keystrings in real code. :(

TEST_KEYSTRING = 'sFbO-GbipIFIpj64S2_AZBIPBvX80Yozszw7PR2dVFg='
TEST_KEYSTRING_WRONG = 'UCPUOddzvewGWaJxW1ZlPKftdlS9SCUjwYUYwov0bT0='

TEST_JSON = os.path.join(CWD, 'test.json')
TEST_JSON_OUTFILE = os.path.join(CWD, 'test.json.enc')


def create_test_json():
    testd = { 'things': {1: 'red', 2: 'blue'}, 'accessories': {'cat': 'hat', 'fish': 'bowl'}}
    open(TEST_JSON, 'w').write(json.dumps(testd))

    ck = CryptKeeper(key=TEST_KEYSTRING)
    open(TEST_JSON_OUTFILE, 'w').write(ck.encrypt(json.dumps(testd)))

def delete_test_json():
    os.remove(TEST_JSON)
    os.remove(TEST_JSON_OUTFILE)    


# ck refers to CryptKeeper objects.
# the CK objects are all thoroughly tested in test_cryptkeeper.py, 
# so here we are testing with just the base (string) class, CryptKeeper

class TestSecureConfig(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        create_test_json()

    @classmethod
    def teardown_class(cls):
    #    delete_test_json()
        pass

    def setUp(self):
        self.ck = CryptKeeper(key=TEST_KEYSTRING)
        self.ck_wrong = CryptKeeper(key=TEST_KEYSTRING_WRONG)

    def test_wrong_ck_raises_InvalidToken(self):
        pass

    def test_write_config_unchanged(self):
        pass

    def test_write_config_encrypted(self):
        pass

    def test_read_enc_without_ck(self):
        pass

