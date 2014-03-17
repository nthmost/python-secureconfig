from json import dumps, loads

from baseclass import SecureConfig

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
    '''Builds a SecureJson object. Requires at minimum a filename or a rawtxt argument.
        
        `readonly` param ensures that .set() and .write() cannot be used. Also ensures that 
        only the resultant configuration structure (not the secrets) remains in memory. When 
        readonly=False, keyloc is retained so that a new encrypted configuration can be created. 
        
        If you don't supply a keyloc, SecureConfig will attempt to read the file as if it
        were stored in plaintext and throw an error if it was encrypted.

        Note: rawtxt / result of open(filepath).read() will never be stored.

        :param filepath:   absolute or relative path to real file on disk.
        :param rawtxt:     string containing encrypted configuration string.
        :param keyloc:     directory location of keyczar managed keys (default: None)
        :param readonly:   protects source config from .write() (default: True)

        :return: SecureConfig object with .cfg dictionary.
    '''
    
    def _fill(self, txt):
        self.cfg = loads(txt)

    def _serialize(self):
        return self.to_json()

    def to_json(self):
        return dumps(self.cfg)



if __name__=='__main__':
    
    testjson = """{
    "thing1": "red",
    "thing2": "blue",
    "secret": "password1",
    "cat": "hat"
}"""

    sjson = SecureJson(rawtxt=testjson, keyloc='.keys', readonly=False)

    sjson.cfg['wet blanket'] = 'the fish'

    print sjson
    
    sjson.write("test_securejson.json.enc")

    newjson = SecureJson(filepath="test_securejson.json.enc", keyloc=".keys", readonly=True)
    print newjson.cfg
    

