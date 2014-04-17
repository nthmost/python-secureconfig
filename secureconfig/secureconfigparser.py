from __future__ import print_function

from configparser import ConfigParser, NoSectionError, NoOptionError

from cryptkeeper import EnvCryptKeeper, FileCryptKeeper

# SECURECONFIG pattern:
#  - allow key retrieval and storage from KEY_STORE object
#  - default to symmetric keys using AES (via Fernet)
#  - (future) provide asymmetric encryption using RSA 


# SECURECONFIGPARSER pattern:
#  - read list of files
#  - read and interpolate vars
#  - has .crypter attribute -> CryptKeeper object

# sec == section


class SecureConfigParser(ConfigParser):
    '''A subclass of ConfigParser py:class::ConfigParser which decrypts certain entries.'''

    def __init__(self, *args, **kwargs):
        if kwargs.get('keystr', None):
            self.ck = CryptKeeper(key=kwargs['keystr'])
        elif kwargs.get('keyenv', None):
            self.ck = EnvCryptKeeper(env=kwargs['keyenv'])
        elif kwargs.get('keypath', None):
            self.ck = FileCryptKeeper(path=kwargs['keypath'])
        else:
            self.ck = None
        super(SecureConfigParser, self).__init__(*args, **kwargs)
    
    def read(self, filenames):
        '''Read the list of config files.'''
        print("[DEBUG] filenames: ", filenames)
        super(SecureConfigParser, self).read(filenames)

    def raw_get(self, sec, key, default=None):
        '''Get the raw value without decoding it.'''
        try:
            return super(SecureConfigParser, self).get(sec, key)
        except (NoSectionError, NoOptionError):
            return default
        except Exception as e:
            print("[DEBUG] e=", sys.exc_info()[0])

#    def raw_set(self, sec, key, val):
#        '''Set the value without encoding it.'''
#        return ConfigParser.set(self, sec, key, val)

#    def raw_items(self, sec):
#        '''Return the items in a section without decoding the values.'''
#        return ConfigParser.items(self, sec)

    def val_decrypt(self, raw_val, **kwargs):
        '''Decode the value.'''
        # determine whether raw_val is plaintext or encrypted.
        # return plaintext value.
        
        try:
            self.ck.crypter.decrypt(raw_val)
        except Exception as e:
            print(e)
            return raw_val

    def get(self, sec, key, default=None):
        '''Get the value from the config, possibly decoding it.'''
        raw_val = self.raw_get(sec, key)
        if raw_val is None:
            return default

        val = self.val_decrypt(raw_val, sec=sec, key=key)
        return val

    def set(self, sec, key, new_val):
        '''If the value should be secured, encode and update it; 
            Otherwise just update it.
        '''
        if not self.has_option(sec, key):
            return self.raw_set(sec, key, val)
        old_raw_val = self.raw_get(sec, key)

        if old_raw_val.startswith(self.ck.sigil):
            new_raw_value = self.crypter.encrypt(old_raw_val)
            return self.raw_set(sec, key, new_raw_val)

        return self.raw_set(sec, key, new_val)

    def items(self, sec):
        '''Iterate over the items; decoding the values.'''
        for (key, val) in self.raw_items(sec):
            val = self.val_decrypt(val, sec=sec, key=key)
            yield (key, val)

    def print_decrypted(self):
        '''Print the file with all the values decoded.'''
        for sec in self.sections():
            print("[%s]" % sec)
        for (key, val) in self.items(sec):
            print("%s=%s" % (key, val))
        print()
