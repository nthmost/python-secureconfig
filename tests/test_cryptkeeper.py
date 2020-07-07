import unittest
import cryptography

from cryptography.fernet import InvalidToken

from secureconfig.cryptkeeper import *

CWD = os.path.dirname(os.path.realpath(__file__))

TEST_KEYSTRING = 'sFbO-GbipIFIpj64S2_AZBIPBvX80Yozszw7PR2dVFg='
TEST_KEYSTRING_WRONG = 'UCPUOddzvewGWaJxW1ZlPKftdlS9SCUjwYUYwov0bT0='

TEST_KEYENV_NAME = 'CK_TEST_KEY'
TEST_KEYFILE_PATH = os.path.join(CWD, 'ck_test_key')

TEST_BAD_KEY = 'YOUR_MOM='


def assure_clean_env():
    os.environ[TEST_KEYENV_NAME] = ''


class TestCryptKeeper(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        assure_clean_env()

    def setUp(self):
        # environment variable used here should be created on the fly.
        self.env_ck = EnvCryptKeeper(TEST_KEYENV_NAME)

        # file will be created in CWD and deleted afterwards.
        self.file_ck = FileCryptKeeper(TEST_KEYFILE_PATH)

        # 
        self.string_ck = CryptKeeper(key=TEST_KEYSTRING)
        self.string_ck_wrong = CryptKeeper(key=TEST_KEYSTRING_WRONG)

    def test_FileCK_creates_keyfile(self):
        assert(os.path.exists(TEST_KEYFILE_PATH))
        with open(TEST_KEYFILE_PATH, 'r') as fh:
            tmp = fh.read().strip().encode()
            fh.close()
        assert(self.file_ck.key == tmp)

    def test_EnvCK_creates_env(self):
        assert(os.environ.get(TEST_KEYENV_NAME, False))
        assert(os.environ.get(TEST_KEYENV_NAME).encode() == self.env_ck.key)

    def test_EnvCK_from_env(self):
        os.putenv('ARBITRARY_ENV_NAME', TEST_KEYSTRING)
        env_ck = EnvCryptKeeper('ARBITRARY_ENV_NAME')
        assert(env_ck.key == os.environ['ARBITRARY_ENV_NAME'].encode())

    def test_FileCK_from_file(self):
        file_ck = FileCryptKeeper(TEST_KEYFILE_PATH)
        with open(TEST_KEYFILE_PATH, 'r') as fh:
            tmp = fh.read().strip().encode()
            fh.close()
        assert(file_ck.key == tmp)

    def test_StringCK_key_eq_key(self):
        self.assertEqual(self.string_ck.key, TEST_KEYSTRING)
    
    def test_bad_key_raises_InvalidToken(self):
        try:
            ck = CryptKeeper(TEST_BAD_KEY)
        except InvalidToken:
            assert True

    def test_wrong_key_raises_InvalidToken(self):
        enctxt = encrypt_string(TEST_KEYSTRING, 'test string')
        self.assertRaises(InvalidToken, self.string_ck_wrong.decrypt, enctxt)

    def test_clean_key(self):
        key_with_whitespace = '\n' + TEST_KEYSTRING + '  '
        assert(self.string_ck._clean_key(key_with_whitespace) == TEST_KEYSTRING)

    def test_generate_key(self):
        new_key = CryptKeeper.generate_key()
        assert(new_key != None)
        #TODO
        #assert(verify_key(new_key))


if __name__ == '__main__':
    assure_clean_env()
    unittest.main()

