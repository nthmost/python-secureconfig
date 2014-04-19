from __future__ import print_function, absolute_import

from ast import literal_eval

from .zeromem import zeromem
from .cryptkeeper import CryptKeeper, EnvCryptKeeper, FileCryptKeeper, cryptkeeper_access_methods
from .exceptions import ReadOnlyConfigError

class SecureString(str):
    '''When garbage collected, leaves behind only a string of zeroes.
    
    (affectionately known as burn-after-reading)'''

    def __init__(self, anystring):
        self._string = anystring
    
    def burn(self):
        zeromem(self._string)
    
    def __del__(self):
        #print("I'm being deleted!")
        zeromem(self._string)

    def __str__(self):
        return self._string
        
    def __repr__(self):
        return self._string


__doc__ = '''SecureConfig base class for simplifying load of encrypted config files (default: serialized dict).

    Features:
    * Instantiate with either a file path or a string of text.
    * Keeps minimum of attributes stored to the object.
    * Access to config variables via .cfg dictionary.
    * ConfigParser-like interface via .get(section, param) method.
    * Default readonly=True protects configuration and "forgets" keyloc.
    * Supply readonly=False to allow use of .set() method.
    
    SecureConfig base class uses only serialized python dictionaries.

    If you want Json specifically, use SecureJson.
'''


class SecureConfig(cryptkeeper_access_methods):
    '''Builds a skeleton SecureConfig object. Not really usable on its own; basically
    provides a common core of classmethods that help set up CryptKeeper methods.
    
    #OLD:
    Requires at minimum a filename or a rawtxt argument.
        
        __init__ requires that you supply a CryptKeeper object, but you can have this part
        handled for you by using the from_env, from_file, and from_key class methods.

        `readonly` param ensures that .set() and .write() cannot be used. 

        If ck==None, SecureConfig will attempt to read the file as if it were stored 
        exclusively in plaintext.

        Note: rawtxt / result of open(filepath).read() will never be stored.

        :param filepath:   absolute or relative path to real file on disk.
        :param rawtxt:     string containing encrypted configuration string.
        :param readonly:   protects source config from .write() (default: True)
        :param ck:         CryptKeeper object (see notes about class methods) 

        :return: SecureConfig object with .cfg dictionary.
    '''

    def __init__(self, filepath='', rawtxt='', readonly=True, **kwargs):

        self.cfg = {}
        self.readonly = readonly
        self.ck = kwargs.get('ck', None)

        if filepath and rawtxt:
            raise SecureConfigException("Supply either filepath or rawtxt (not both).")

        if filepath:
            rawtxt = self._read(filepath)

        #TODO: work out more specific Exceptions
        try:
            self._fill(self._decrypt(rawtxt))
        except Exception as e:
            # if self.ck is None or rawtxt is not encrypted
            self._fill(rawtxt)

    def _decrypt(self, buf):
        return self.ck.crypter.decrypt(buf)

    def _encrypt(self, buf):
        return self.ck.crypter.encrypt(buf)

    def _fill(self, txt=''):
        self.cfg = literal_eval(txt)

    def _read(self, filepath):
        return open(filepath, "rb" ).read()

    def _serialize(self):
        return '%r' % self.cfg

    def __repr__(self):
        return '%r' % self.cfg
       
    def get(self, section, param):
        '''provides ConfigParser-like interface retrieve variables from sections.

        If your config data is shallow, i.e. non-hierarchical, either a TypeError
        or a NameError will be thrown (depending on your data).

        :param section:  top-level "section" of configuration.
        :param param:    parameter within "section" whose value will be returned.

        '''
        return self.cfg['section']['param']

    def set(self, section, param, value):
        '''complement of .get(), allows change to configuration dictionary if .readonly=False.

        If your config data is shallow, i.e. non-hierarchical, a TypeError will be thrown.

        :param section:  top-level "section" of configuration.
        :param param:    parameter to set within "section".
        :param value:    new value for param.
        '''
        if self.readonly:
            raise ReadOnlyConfigError
        else:
            self.cfg[section][param] = value

    def write(self, filepath=''):
        if self.readonly:
            raise ReadOnlyConfigError

        try:
            buf = self._encrypt(self._serialize())
        except AttributeError:
            # no self.crypter because no keyloc supplied
            buf = self._serialize()

        if filepath=='':
            filepath = self.filepath

        f=open(filepath, 'wb')
        f.write(buf)
        f.close()
