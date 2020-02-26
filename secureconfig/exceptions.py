class SecureConfigException(Exception):
    def __init__(self, message, Errors=[]):
        Exception.__init__(self, message)
        self.Errors = Errors


class ReadOnlyConfigError(SecureConfigException):
    pass
