import os, string
from random import sample, choice

# all ck_obj arguments refer to instances of CryptKeeper objects (and subclass objects)

ACCEPTED_SYMBOLS = '_-)(&^#@!.'


def safe_pwgen(length=32, symbols=ACCEPTED_SYMBOLS):
    """returns a non-human-readable password of length=length (default 32).

        :param length: (int) desired length of password (default: 32)
        :param symbols: non-alphanumeric symbols to accept as part of the password.
                default ACCEPTED_SYMBOLS=  _-)(&^#@!.
        """
    chars = string.letters + string.digits + symbols
    return ''.join(choice(chars) for _ in range(length))


def encrypt_file(ck_obj, infile, outfile):
    enctxt = ck_obj.encrypt(open(infile, 'r').read())
    f = open(outfile, 'wb')
    f.write(enctxt)
    f.close()


def decrypt_file(ck_obj, infile, outfile=''):
    txt = ck_obj.decrypt(open(infile, 'rb').read())
    if outfile:
        f = open(outfile, 'w')
        f.write(txt)
        f.close()
        return outfile
    else:
        return txt
