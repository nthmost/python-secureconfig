from __future__ import print_function

import unittest
import cryptography
from ConfigParser import ConfigParser

from cryptography.fernet import InvalidToken

from secureconfig.cryptkeeper import *
from secureconfig.secureconfigparser import SecureConfigParser

CWD = os.path.dirname(os.path.realpath(__file__))

# please don't use any of these keystrings in real code. :(

TEST_KEYSTRING = 'sFbO-GbipIFIpj64S2_AZBIPBvX80Yozszw7PR2dVFg='
TEST_KEYSTRING_WRONG = 'UCPUOddzvewGWaJxW1ZlPKftdlS9SCUjwYUYwov0bT0='

TEST_INI = os.path.join(CWD, 'cfg_test.ini')
TEST_INI_OUTFILE = os.path.join(CWD, 'cfg_test_out.ini')


def create_test_ini():
    # create cfg_test.ini in testing directory
    open(TEST_INI, 'w').write('''[database]
username=some_user
password=lame_password
hostname=some_hostname
port=3306
''')


def encrypt_password(config, new_val='lame_password'):
    cfg.set('database', 'password', new_val, True)
    return cfg

    print(cfg.raw_get('database', 'password'))

    print('\ncfg.get returns:')
    print(cfg.get('database', 'password'))
    cfg.write(open(TEST_INI_OUTFILE, 'w'))


def decrypt_password(ck_obj):
    cfg = SecureConfigParser(ck=ck_obj)
    cfg.read(TEST_INI_OUTFILE)

    try:
        print(cfg.get('database', 'password'))
    except InvalidToken:
        print('wrong key for this config file')


def assure_clean_env():
    os.environ[TEST_KEYENV_NAME] = ''

def delete_test_ini():
    os.remove(TEST_INI_INPUT)
    if os.path.exists(TEST_INI_OUTFILE):
        os.remove(TEST_INI_OUTFILE)

# what passes for a "fixture" in this test module.
testd = {     'section': 'database',
              'plain': { 'key': 'username', 'raw_val': 'some_user'},
              'enc': {'key': 'password', 'raw_val': 'lame_password'},
            }
# ck refers to CryptKeeper objects.
# the CK objects are all thoroughly tested in test_cryptkeeper.py, 
# so here we are testing with just the base (string) class, CryptKeeper

class TestSecureConfigParser(unittest.TestCase):

    @classmethod
    def setup_module(cls):
        create_test_ini()

    @classmethod
    def teardown_module(cls):
        pass
        #delete_test_ini()

    def setUp(self):
        self.ck = CryptKeeper(key=TEST_KEYSTRING)
        self.ck_wrong = CryptKeeper(key=TEST_KEYSTRING_WRONG)

    def test_wrong_ck_raises_InvalidToken(self):
        scfg = SecureConfigParser(ck=self.ck_wrong)
        scfg.read(TEST_INI_OUTFILE)
        self.assertRaises(InvalidToken, scfg.get(testd['section'], testd['enc']['key'])) 

    def test_get_plaintext_value_is_plaintext(self):
        scfg = SecureConfigParser(ck=self.ck)
        scfg.read(TEST_INI)
        plainval = scfg.get(testd['section'], testd['plain']['key'])
        assert plainval == testd['plain']['raw_val']

    def test_get_encrypted_value_is_encrypted(self):
        pass

    def test_set_encrypted_value_is_encrypted(self):
        scfg = SecureConfigParser(ck=self.ck)
        scfg.read(TEST_INI)
        scfg.set(testd['section'], testd['enc']['key'], testd['enc']['raw_val'], encrypt=True)
        
        result = scfg.raw_get(testd['section'], testd['enc']['key']) 
        self.assertFalse(result == testd['enc']['raw_val'])
        self.assertTrue(result.startswith(scfg.ck.sigil))
        self.assertTrue(scfg.get(testd['section'], testd['enc']['key']) == testd['enc']['raw_val'])

    def test_write_config_with_new_encrypted_values(self):
        scfg = SecureConfigParser(ck=self.ck)
        scfg.read(TEST_INI)
        scfg.set(testd['section'], testd['enc']['key'], testd['enc']['raw_val'], encrypt=True)
  


    def test_write_config_unchanged(self):
        fh=open(TEST_INI_OUTFILE, 'w')
        scfg = SecureConfigParser()
        scfg.read(TEST_INI)
        scfg.write(fh)
        fh.close()

        self.assertTrue(os.path.exists(TEST_INI_OUTFILE))
        cfg = ConfigParser()
        cfg.read(TEST_INI_OUTFILE)
        assert(cfg.get(testd['section'], testd['plain']['key'] == testd['plain']['raw_val']))
        os.remove(TEST_INI_OUTFILE)

