# stubs of ideas for decorators


def encrypted(func):
    """make sure data transmissions are encrypted"""
    return func


def protected(func):
    """makes sure files are encrypted when written, and uses decrypt when read."""
    return func


