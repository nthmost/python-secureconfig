from __future__ import absolute_import
from ast import literal_eval

from .cryptkeeper import CryptKeeper, EnvCryptKeeper, FileCryptKeeper, cryptkeeper_access_methods
from .exceptions import ReadOnlyConfigError, SecureConfigException

__doc__ = '''SecureConfig base class for simplifying load of encrypted config files (default: serialized dict).

    Features:
  
    * Instantiate with either a file path or a string of text (or none for a blank slate).
    * Stores simple "config" dictionary in .cfg
    * ConfigParser-like interface (get, set, add_section, remove_section, write)
    * .write(filehandle) method serializes dictionary, encrypts, and writes to open filehandle
    * Supply readonly=True to protect configuration from .set and .write
    
    SecureConfig base class uses only serialized python dictionaries.

    For JSON, use SecureJson.
    For .ini-style files, use SecureConfigParser.
'''


class SecureConfig(cryptkeeper_access_methods):
    """Builds a SecureConfig object.

    Without any arguments, SecureConfig.__init__ is a blank slate into which you can
    load dictionary-based data directly into cfg.

    To decrypt data, SecureConfig requires a CryptKeeper object, but the following class
    methods help set this up for you:

        SecureConfig.from_key(keystring)
        SecureConfig.from_file(keyfilename)
        SecureConfig.from_env(key_environment_variable_name)

    Otherwise, supply a CryptKeeper object directly:

        SecureConfig(ck=CryptKeeper(key=some_key))

    If ck==None, SecureConfig will attempt to read the file as if it were stored
    exclusively in plaintext and throws SecureConfigException if it cannot be parsed.

    `readonly` param ensures that .set() and .write() cannot be used.

        :param filepath:   absolute or relative path to real file on disk.
        :param rawtxt:     string containing encrypted configuration string.
        :param readonly:   protects source config from .write() (default: False)
        :param ck:         CryptKeeper object (see secureconfig.cryptkeeper)

        :return: SecureConfig object with .cfg dictionary.
    """

    def __init__(self, filepath='', rawtxt='', readonly=False, **kwargs):

        self.cfg = {}
        self.readonly = readonly
        self.ck = kwargs.get('ck', None)

        if filepath and rawtxt:
            raise SecureConfigException('Supply either filepath or rawtxt (not both).')

        if filepath:
            rawtxt = self._read(filepath)

        if self.ck and rawtxt:
            self._fill(self._decrypt(rawtxt))        
        elif rawtxt:
            try:
                self._fill(rawtxt)
            except ValueError:
                # invalid data structure OR this file was encrypted.
                # This approach may only work for SecureJson, which so far is the only use 
                # for this base class. Please rework as needed to better generalize.
                raise SecureConfigException('bad data or missing encryption key')                  
        else:
            # this is a "blank slate" configuration.
            self.cfg = {}

    def _decrypt(self, buf):
        return self.ck.crypter.decrypt(buf).decode()

    def _encrypt(self, buf):
        return self.ck.crypter.encrypt(buf.encode()).decode()

    def _fill(self, txt=''):
        self.cfg = literal_eval(txt)

    def _read(self, filepath):
        with open(filepath, 'rb') as fh:
            tmp = fh.read()
            fh.close()
        return tmp

    def _serialize(self):
        return '%r' % self.cfg

    def __repr__(self):
        return '%r' % self.cfg
       
    def get(self, section, param):
        """provides ConfigParser-like interface retrieve variables from sections.

        If your config data is shallow, i.e. non-hierarchical, either a TypeError
        or a NameError will be thrown (depending on your data).

        :param section:  top-level "section" of configuration.
        :param param:    parameter within "section" whose value will be returned.

        """
        return self.cfg[section][param]

    def remove_section(self, section):
        """Remove the specified section from the configuration. If the section in fact
            existed, return True. Otherwise return False."""
        try:
            self.cfg.pop(section)
            return True
        except KeyError:
            return False

    def add_section(self, section):
        """Add a section named section to the instance."""
        if self.cfg.get(section, None):
            raise SecureConfigException('specified section already exists')
        else:
            self.cfg[section] = {}            

    def sections(self):
        """Returns a list of available sections in the config."""
        return list(self.cfg.keys())

    def options(self, section):
        """Returns a list of options available in the specified section."""
        return list(self.cfg[section].keys())

    def set(self, section, param, value):
        """if .readonly=False, allows set of param in "section" to value.

        If your config data is 1-dimensional, TypeError will be thrown.

        If "section" does not exist, KeyError will be thrown.

        :param section:  top-level "section" of configuration.
        :param param:    parameter to set within "section".
        :param value:    new value for param.
        """
        if self.readonly:
            raise ReadOnlyConfigError
        else:
            self.cfg[section][param] = value

    def write(self, fh=None):
        """if .readonly=False, serializes, encrypts (if key) writing to specified filehandle."""
        if self.readonly:
            raise ReadOnlyConfigError
        try:
            buf = self._encrypt(self._serialize())
        except AttributeError:
            # no self.ck / no key supplied
            buf = self._serialize()
        fh.write(buf)
