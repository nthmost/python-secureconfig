# Always prefer setuptools over distutils
# To use a consistent encoding
from codecs import open
import os
from setuptools import setup, find_packages
from distutils.core import Extension

here = os.path.abspath(os.path.dirname(__file__))

os.environ['ARCHFLAGS'] = '-Wno-error=unused-command-line-argument-hard-error-in-future'

try:
    from Cython.Distutils import build_ext
except ImportError:
    from distutils.command import build_ext
    use_cython = False
else:
    use_cython = True

cmdclass = {}
ext_modules = []

# make sure Cython code is always freshened up before sdist upload.
from distutils.command.sdist import sdist as _sdist


class sdist(_sdist):
    def run(self):
        # Make sure the compiled Cython files in the distribution are up-to-date
        from Cython.Build import cythonize
        print("cythonizing...")
        cythonize(['cython/mycythonmodule.pyx'])
        _sdist.run(self)


cmdclass['sdist'] = sdist

if use_cython:
    ext_modules += [Extension('secureconfig.zeromem', sources=['secureconfig/zeromem.pyx']), ]
    cmdclass.update({'build_ext': build_ext})
    print(cmdclass)
else:
    ext_modules += [Extension('secureconfig.zeromem', sources=['secureconfig/zeromem.c']), ]


# Version info -- read without importing
_locals = {}
with open("secureconfig/_version.py") as fp:
    exec(fp.read(), None, _locals)
version = _locals["__version__"]

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="secureconfig",
    version=version,
    description="Configuration-oriented encryption toolkit to make secure config files simple",
    long_description=long_description,
    url="https://bitbucket.org/nthmost/python-secureconfig",
    author="Naomi Most",
    author_email="naomi@nthmost.net",
    maintainer="Naomi Most",
    maintainer_email="naomi@nthmost.net",
    cmdclass=cmdclass,
    ext_modules=ext_modules,
    license="MIT",
    zip_safe=True,
    packages=find_packages(),
    install_requires=[
        'cryptography',
        'configparser',
        'pycrypto',
        'pyasn1'
    ],
)

