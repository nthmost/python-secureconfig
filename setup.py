from setuptools import setup, find_packages
#from distutils.extension import Extension
from distutils.core import Extension

import os
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
        print "cythonizing..."
        cythonize(['cython/mycythonmodule.pyx'])
        _sdist.run(self)
cmdclass['sdist'] = sdist

if use_cython:
    ext_modules += [ Extension('secureconfig.zeromem', sources=['secureconfig/zeromem.pyx']), ]
    cmdclass.update({ 'build_ext': build_ext })
    print cmdclass
else:
    ext_modules += [ Extension('secureconfig.zeromem', sources=['secureconfig/zeromem.c']), ]


setup (
    name = "secureconfig",
    version = "0.1.2",
    description = "Configuration-oriented encryption toolkit to make secure config files simple",
    url="https://bitbucket.org/nthmost/python-secureconfig",
    author = "Naomi Most",
    author_email = "naomi@nthmost.net",
    maintainer = "Naomi Most",
    maintainer_email = "naomi@nthmost.net",
    cmdclass = cmdclass,
    ext_modules = ext_modules,
    license = "MIT",
    zip_safe = True,
    packages = find_packages(),
    install_requires = [ 'cryptography', 'configparser' ],
    )

