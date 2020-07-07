from .zeromem import zeromem


class SecureString(str):
    """When garbage collected, leaves behind only a string of zeroes."""

    def __init__(self, anystring):
        super().__init__()
        self._string = bytes(anystring, 'utf-8')

    def burn(self):
        zeromem(self._string)

    def __del__(self):
        # print("I'm being deleted!")
        zeromem(self._string)

    def __str__(self):
        return self._string
        
    def __repr__(self):
        return self._string
