from ast import literal_eval

from cryptkeeper import CryptKeeper, EnvCryptKeeper, FileCryptKeeper
from exceptions import *

__author__ = 'nthmost'

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

class SecureConfig(object):
    '''Builds a SecureConfig object. Requires at minimum a filename or a rawtxt argument.
        
        `readonly` param ensures that .set() and .write() cannot be used.  Also ensures that 
        only the resultant configuration structure remains in memory. When readonly=False, 
        keyloc is retained so that a new encrypted configuration can be created. 

        Note: rawtxt / result of open(filepath).read() will never be stored.

        :param filepath:   absolute or relative path to real file on disk (overrides rawtxt).
        :param rawtxt:     string containing encrypted configuration string.
        :param keyloc:     directory location of keyczar managed keys.
        :param readonly:   protects source config from .write() (default: True)

        :return: SecureConfig object with .cfg dictionary.
    '''

    @classmethod
    def from_env(cls, env, filepath='', rawtxt='', readonly=True, **kwargs):
        ck_obj = EnvCryptKeeper(env)
        return cls.__init__(ck_obj, *args, **kwargs)

    @classmethod
    def from_file(cls, keyfilename, filepath='', rawtxt='', readonly=True, **kwargs):
        ck_obj = FileCryptKeeper(keyfilename)
        return cls.__init__(ck_obj, *args, **kwargs)

    @classmethod
    def from_key(cls, keystring, *args, **kwargs):
        ck_obj = CryptKeeper(keystring)
        return cls.__init__(ck_obj, *args, **kwargs)

    def __init__(self, ck_obj=None, filepath='', rawtxt='', readonly=True):

        self.cfg = {}
        self.readonly = readonly
        self.ck = self.ck_obj

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
        finally:
            


    def _decrypt(self, buf):
        return self.ck.crypter.decrypt(buf)

    def _encrypt(self, buf):
        return self.ck.crypter.encrypt(buf)

    def _fill(self, txt=''):
        self.cfg = literal_eval(txt)

    def _read(self, filepath):
        return open(filepath, "rb" ).read()

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

    def _serialize(self):
        return '%r' % self.cfg

    def __repr__(self):
        return '%r' % self.cfg

