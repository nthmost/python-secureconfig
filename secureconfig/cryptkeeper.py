from __future__ import print_function

import os
from cryptography.fernet import Fernet, InvalidToken


# CryptKeeper pattern:
#  - location possibilities: file, env, string
#  - schemes: symmetric (AES) via Fernet [future: asymmetric (RSA)]
#  - actions: load, store, encrypt, decrypt.

# Notes:
#
# Assume "aspirational" invocation of $StorageCryptKeeper unless 
# kwargs['proactive'] == False
# (i.e. if supplied file path or env variable doesn't exist, create it.)
#
# FileCryptKeeper will not create a directory, only a file. Target directory must exist.
#

class CryptKeeper(object):
    sigil = 'CK_FERNET_::'

    def __init__(self, *args, **kwargs):
        '''base CryptKeeper class. Supply key=string to provide key,
        or allow CryptKeeper to generate a new key when instantiated 
        without arguments.'''
    
        if kwargs.get('key', None):
            self.key = kwargs['key']
        
        # if proactive==True, create storage destination for key.
        # Appropriate Exception will be raised if store() not possible.
        
        self.proactive = kwargs.get('proactive', False)

        if self._key_exists():
            self.key = self.load()
            self.crypter = Fernet(self.key)
        elif self.proactive:
            self.gen_key()
            self.crypter = Fernet(self.key)
            self.store()
        else:
            raise Exception('key location does not exist')

    def _key_exists(self):
        'override for key storage based classes'
        if self.key:
            return True

    def gen_key(self):
        'generates a new Fernet-based encryption key and assigns it to self.key'
        self.key = Fernet.generate_key()
        return self.key
        
    def encrypt(self, inp):
        'takes plaintext string and returns encrypted string'
        return self.crypter.encrypt(inp)
        
    def decrypt(self, inp):
        'takes encrypted string and returns plaintext string' 
        return self.crypter.decrypt(inp)
    
    def store(self):
        'override for key storage based classes'
        pass
        
    def load(self):
        'override for key storage based classes'
        return self.key



class EnvCryptKeeper(CryptKeeper):
    sigil = 'CK_ENV_::'

    def __init__(self, env, *args, **kwargs):
        '''Loads a key from env.  If proactive==True (default: False) and no key is 
        present at env, EnvCryptKeeper creates a key for you at this environment 
        variable.'''
    
        self.env = env
        super(EnvCryptKeeper, self).__init__(*args, **kwargs)
            
    def _key_exists(self):
        return os.environ.get(self.env, None)

    def store(self):
        'store currently active key into environment variable'
        os.environ[self.env] = self.key
    
    def load(self):
        'retrieve key from environment variable'
        return os.environ[self.env]


class FileCryptKeeper(CryptKeeper):
    sigil = 'CK_PATH_::'

    def __init__(self, path, *args, **kwargs):
        '''loads a key from supplied path.
        
        If proactive==True (default: False) and file cannot be loaded at
        supplied path, FileCryptKeeper creates this file to store key within.
        
        If directory cannot be written to, FileCryptKeeper raises OSError
        (i.e. it will not also try to create a directory.)

        Supply paranoid=False to turn off directory permission checks.
        (DANGER, WILL ROBINSON!)        
        '''
        
        self.path = path    
        self.paranoid = kwargs.get('paranoid', True)
        super(FileCryptKeeper, self).__init__(*args, **kwargs)

    def _key_exists(self):
        #TODO TODO TODO
        #if self.paranoid:
        #   check permissions on file and path.
        #   if sketchy, raise Exception informing user of sketchiness.
        return os.path.exists(self.path)
        
    def store(self):
        'store currently active key into file at self.path'
        open(self.path, 'wb').write(self.key)
    
    def load(self):
        'retrieve key from file at self.path (supplied at instantiation)'
        return open(self.path, 'rb').read()

