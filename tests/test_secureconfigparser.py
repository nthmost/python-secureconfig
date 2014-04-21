from __future__ import print_function

import unittest
import cryptography

from cryptography.fernet import InvalidToken

from secureconfig.cryptkeeper import *
from secureconfig.secureconfigparser import SecureConfigParser

CWD = os.path.dirname(os.path.realpath(__file__))

# please don't use any of these keystrings in real code. :(

TEST_KEYSTRING = 'sFbO-GbipIFIpj64S2_AZBIPBvX80Yozszw7PR2dVFg='
TEST_KEYSTRING_WRONG = 'UCPUOddzvewGWaJxW1ZlPKftdlS9SCUjwYUYwov0bT0='

TEST_SECURECONFIGPARSER_INPATH = os.path.join(CWD, 'cfg_test.ini')
TEST_SECURECONFIGPARSER_OUTPATH = os.path.join(CWD, 'cfg_test_out.ini')


def create_test_ini():
    # create cfg_test.ini in testing directory
    open(TEST_SECURECONFIGPARSER_INPATH, 'w').write('''[database]
username=testuser
password=lame_password
hostname=some_hostname
port=3306
db_connection_string=mysql://locuslibrary:locuslibrary@db-prd.locusdev.net/locuslibrary
''')


def encrypt_password(ck_obj):
    cfg = SecureConfigParser(ck=ck_obj)
    cfg.read(TEST_SECURECONFIGPARSER_INPATH)
    cfg.set('database', 'password', 'locuslibrary', True)

    print('New line in config:')
    print(cfg.raw_get('database', 'password'))

    print('\ncfg.get returns:')
    print(cfg.get('database', 'password'))
    cfg.write(open(TEST_SECURECONFIGPARSER_OUTPATH, 'w'))


def decrypt_password(ck_obj):
    cfg = SecureConfigParser(ck=ck_obj)
    cfg.read(TEST_INI_OUTPUT)

    try:
        print(cfg.get('database', 'password'))
    except InvalidToken:
        print('wrong key for this config file')


def assure_clean_env():
    os.environ[TEST_KEYENV_NAME] = ''

def delete_test_ini():
    os.remove(TEST_INI_INPUT)
    os.remove(TEST_INI_OUTPUT)


# ck refers to CryptKeeper objects.
# the CK objects are all thoroughly tested in test_cryptkeeper.py, 
# so here we are testing with just the base (string) class, CryptKeeper

class TestSecureConfigParser(unittest.TestCase):
    testd = { 'section': 'database',
              'keyname': 'password',
              'raw_val': 'lame_password',
              'enc_val': 'gAAAAABTUZkkvlVWGrDhp0NM0HL9mBWcUPcnAw57E7QojIFuQZkq7xSJPqLCArDh3LFOTXWwIhXnlRvsdzwwxmCTq55E9uzbvg==',
              'Fernet_key': TEST_KEYSTRING,
            }

    def setUp(self):
        #
        os.remove(TEST_INI_OUTPUT)

        self.ck = CryptKeeper(key=TEST_KEYSTRING)
        self.ck_wrong = CryptKeeper(key=TEST_KEYSTRING_WRONG)

        self.cfg_no_ck = SecureConfigParser()
        self.


    def test_SecureConfigParser_no_ck_raises_Exception():
        

    def test_SCP_wrong_ck_raises_Exception():


    def test_plaintext_value_is_plaintext(self):
        pass    

    def test_get_encrypted_value_is_encrypted(self):
        pass

    def test_set_encrypted_value_is_encrypted(self):
        pass

    def test_write_config_unchanged(self):
        fh=open(TEST_SECURECONFIGPARSER_OUTFILE)
        self.cfg_no_ck.write(



if __name__ == '__main__':
    create_test_ini()
    unittest.main()
    delete_test_ini()
    delete_test_json()

