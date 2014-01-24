from setuptools import setup, find_packages

setup(
    name = "python-secureconfig",
    version = "0.0.1",
    description = "SecureConfig toolkit making encrypted config files easy.",
    url="https://bitbucket.org/nthmost/python-secureconfig",
    author = "Naomi Most",
    author_email = "naomi@nthmost.net",
    maintainer = "Naomi Most",
    maintainer_email = "naomi@nthmost.net",
    license = "MIT",
    zip_safe = True,
    packages = find_packages(),
    install_requires = [ 'python-keyczar',
                        ],
    )
