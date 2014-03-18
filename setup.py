from setuptools import setup, find_packages
#from distutils.extension import Extension
from distutils.core import Extension

from Cython.Distutils import build_ext

setup(
    name = "secureconfig",
    version = "0.0.1",
    description = "Configuration-oriented encryption toolkit to make secure config files simple",
    url="https://bitbucket.org/nthmost/python-secureconfig",
    cmdclass = {'build_ext': build_ext},
    author = "Naomi Most",
    author_email = "naomi@nthmost.net",
    maintainer = "Naomi Most",
    maintainer_email = "naomi@nthmost.net",
    ext_modules=[Extension('zeromem', sources=['secureconfig/zeromem.c'])],
    license = "MIT",
    zip_safe = True,
    packages = find_packages(),
    install_requires = [
                         'Cython',
                         'python-keyczar',
                        ],
    )
