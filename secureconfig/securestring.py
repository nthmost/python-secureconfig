from __future__ import print_function, absolute_import
import six
from .zeromem import zeromem


class SecureString(str):
    """When garbage collected, leaves behind only a string of zeroes."""

    def __init__(self, anystring):
        super().__init__()
        self._string = anystring

    def burn(self):
        if six.PY3:
            zeromem(self._string.encode())
        else:
            zeromem(self._string)

    def __del__(self):
        # print("I'm being deleted!")
        if six.PY3:
            zeromem(self._string.encode())
        else:
            zeromem(self._string)

    def __str__(self):
        return self._string
        
    def __repr__(self):
        return self._string

