import os

from keyczar import keyczar, keyczart
from keyczar.errors import KeyczarError


FMT_CREATE = 'create --location=%(loc)s --purpose=crypt'
FMT_ADDKEY = 'addkey --location=%(loc)s --status=primary'


def initialize_keys(keyloc):
    _require_dir(keyloc)
    pass

def encrypt_file(keyloc, infile, outfile=''):
    f=open(infile, 'rb')
    crypter = keyczar.Crypter.Read(keyloc)


def decrypt_file(keyloc, infile, outfile=''):
    crypter = keyczar.Crypter.Read(keyloc)
    


def _require_dir(keyloc):
    '''Make sure that keyloc is a directory.
    If it does not exist, create it.
    '''
    if os.path.exists(keyloc):
        if not os.path.isdir(keyloc):
            raise ValueError('%s must be a directory' % keyloc)
    else:
        os.makedirs(keyloc, 0700)


def _tool(fmt, **kwds):
    '''Package the call to keyczart.main
    which is awkwardly setup for command-line use without
    organizing the underlying logic for direct function calls.
    '''
    return keyczart.main( (fmt % kwds).split() )

def _initialize(keyloc, **kwds):
    '''Initialize a location
    create it
    add a primary key
    '''
    _require_dir(keyloc)
    steps = [KEYCZAR_CREATE, KEYCZAR_ADDKEY]
    for step in steps:
        _tool(step, loc=loc, **kwds)



