from json import dumps, loads

from .baseclass import SecureConfig

__doc__ = '''SecureJson class for simplifying load of encrypted config files.

    Subclassed from SecureConfig.

    Features:
    * Instantiate with either a file path or a string of text.
    * Keeps minimum of attributes stored to the object.
    * Access to config variables via .cfg dictionary.
    * ConfigParser-like interface via .get(section, param) method.
    * Default readonly=True protects configuration and "forgets" keyloc.
    * Supply readonly=False to allow use of .set() method.
'''


class SecureJson(SecureConfig):
    """Builds a SecureJson object. Requires at minimum a filename or a rawtxt argument.

        __init__ requires that you supply a CryptKeeper object, but you can have this part
        handled for you by using the from_env, from_file, and from_key class methods.

        `readonly` param ensures that .set() and .write() cannot be used.

        If ck_obj==None, SecureConfig will attempt to read the file as if it
        were stored in plaintext and throw an error if it was encrypted.

        Note: rawtxt / result of open(filepath).read() will never be stored.

        :param ck_obj:     CryptKeeper object (see notes about class methods)
        :param filepath:   absolute or relative path to real file on disk.
        :param rawtxt:     string containing encrypted configuration string.
        :param readonly:   protects source config from .write() (default: True)

        :return: SecureJson object with .cfg dictionary.
    """
    
    def _fill(self, txt):
        self.cfg = loads(txt)

    def _serialize(self):
        return self.to_json()

    def to_json(self):
        return dumps(self.cfg)


if __name__ == '__main__':
    
    testjson = """{
    "thing1": "red",
    "thing2": "blue",
    "secret": "password1",
    "cat": "hat"
}"""

    sjson = SecureJson(rawtxt=testjson, keyloc='.keys', readonly=False)

    sjson.cfg['wet blanket'] = 'the fish'

    print(sjson)
    
    sjson.write("test_securejson.json.enc")

    newjson = SecureJson(filepath="test_securejson.json.enc", keyloc=".keys", readonly=True)
    print(newjson.cfg)
