from __future__ import print_function

import unittest, os, json

from cryptography.fernet import InvalidToken

from secureconfig.cryptkeeper import *
from secureconfig import SecureConfig, SecureJson
from secureconfig import SecureConfigException

CWD = os.path.dirname(os.path.realpath(__file__))

# please don't use any of these keystrings in real code. :(

TEST_KEYSTRING = 'sFbO-GbipIFIpj64S2_AZBIPBvX80Yozszw7PR2dVFg='
TEST_KEYSTRING_WRONG = 'UCPUOddzvewGWaJxW1ZlPKftdlS9SCUjwYUYwov0bT0='

TEST_JSON = os.path.join(CWD, 'test.json')
TEST_JSON_OUTFILE = os.path.join(CWD, 'test.json.enc')


def create_test_json():
    print('Creating JSON file')
    testd = { 'things': {1: 'red', 2: 'blue'}, 'accessories': {'cat': 'hat', 'fish': 'bowl'}}
    open(TEST_JSON, 'w').write(json.dumps(testd))

    ck = CryptKeeper(key=TEST_KEYSTRING)
    open(TEST_JSON_OUTFILE, 'w').write(ck.encrypt(json.dumps(testd)))

def delete_test_json():
    os.remove(TEST_JSON)
    os.remove(TEST_JSON_OUTFILE)    


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

    def test_write_config_unchanged(self):
        # refers to code that will be implemented in secureconfig 0.0.5
        pass

    def test_write_config_encrypted(self):
        # refers to code that will be implemented in secureconfig 0.0.5
        pass

    def test_read_enc_without_key_raises_SecureConfigException(self):
        'bad data or missing key'
        kwargs = { 'filepath': TEST_JSON_OUTFILE }
        self.assertRaises(SecureConfigException, SecureJson, **kwargs )
        
    def test_read_enc_wrong_key_raises_InvalidToken(self):
        'ValueError: No JSON object could be decoded'
        args = [TEST_KEYSTRING_WRONG]
        kwargs = { 'filepath': TEST_JSON_OUTFILE }
        self.assertRaises(InvalidToken, SecureJson.from_key, *args, **kwargs) 

    def test_read_enc_with_ck_produces_cfg(self):
        sj = SecureJson.from_key(TEST_KEYSTRING, filepath=TEST_JSON_OUTFILE)
        self.assertTrue( type(sj.cfg)== type({}) )


if __name__ == '__main__':
    create_test_json()
    unittest.main()
