************
secureconfig
************

by Naomi Most (@nthmost)

A simple solution to the often annoying problem of protecting config files.

secureconfig makes keeping your secrets secure on servers and source control 
repositories easy by restricting your choices on the matter, defaulting to 
a "medium-high paranoia" set of operations.

Those choices, specifically::

   Use AES-128 CBC via Fernet (see https://cryptography.io/en/latest/fernet/ )
   Store keys in environment variables, or in files protected by the system.
   Provide an easy way to overwrite sensitive string data left behind by with zeroes.

This library has undergone an overhaul since last version, so if you were using 0.0.2.x,
please read the below carefully so you understand what has changed (A LOT!).

The major philosophical shift was to separate the duties of encryption and data 
structure handling into the CryptKeeper classes and SecureConfig* classes. This means 
that if you just want a consistent way to encrypt/decrypt strings and files that works
across all of your data structures, the CryptKeeper classes will come in handy.

Config styles currently supported::

    ConfigParser (see SecureConfigParser)
    Json (see SecureJson) -- whole-data encryption only.
    serialized dictionaries (see SecureConfig) -- whole-data encryption only.

If you'd like to see another type supported, please file a feature request on GitHub
at https://github.com/nthmost/python-secureconfig

Purpose
-------

secureconfig is being developed in the context of an open-source-loving,
"information wants to be free" kind of company that also does not wish to 
get totally pwned in a heartbeat when, say, bitbucket has a major security
breach. 

We have a lot of pre-existing code that makes use of ConfigParser ini-style
files and also JSON config files. The best solution for protecting our 
services and sensitive information would be to create a drop-in replacement
for ConfigParser that allows us to keep 99% of the way we interact with
config files, and simply wraps the decryption step.

Of course, once you have decryption handled, you start to want simplified 
ways of encrypting as well.  That's why secureconfig supports writing new
config files.

See "basic usage" sections below to see how you can easily turn a plaintext
value or file into an encrypted value or file (depending on config style).

The CryptKeeper classes can even generate new keys for you.  Just make sure 
you keep track of which keys match with your data; this library will not stop
you from shooting yourself in the foot!

secureconfig also tries to be helpful in keeping stored keys secure. FileCryptKeeper
has "paranoid" mode on by default, which means that it will check to see whether the
key is in a directory protected by your operating system. If not, it will refuse to
run.  (Turn this off using paranoid=False, if you must.)

Finally, secureconfig contains a smattering of deployment utilities found in 
secureconfig.utils.  Feel free to suggest new ones.

Contributions and code/documentation critiques are warmly welcomed.
See the Contribution section below for information.


How secureconfig Works
----------------------

At its core, secureconfig simply subclasses the configuration mechanisms we 
all know and love, and wraps certain operations (read-from-file and/or 
read-and-interpolate) in a decryption layer.

This library bases its operations on Fernet, a cryptography meta-protocol (see
https://cryptography.io) developed to help programmers choose the best possible
defaults for their encryption tasks.

The CryptKeeper classes handle key storage, en/decryption, and key generation.
All SecureConfig* classes receive from_x class instantiation methods to set up
an internal CryptKeeper. 

Table of Methods of key storage - CryptKeeper class - SecureConfig* classmethod:: 

    string -- CryptKeeper -- .from_key(key_string)
    file -- FileCryptKeeper -- .from_file(key_filename)
    environment variable -- EnvCryptKeeper -- .from_env(key_env_name)

All CryptKeeper classes have a default argument of `proactive=True`, which means
that the CryptKeeper instance will try to store a key in that place whether it
currently exists or not.  If this place is not writeable, you'll get your OS's usual
error for an attempted operation.

When proactive=False and locations do not exist, you'll get a KeyError for environment
variables or an OSError for files.

If CryptKeeper classes are instantiated without a key argument, they will generate
a key automatically for you. 

Another way to generate a new key is to use the CryptKeeper classmethod `.generate_key()`.

NOTICE:  You can't assign a new key to a CryptKeeper object after it's been created and
have it work. (If that seems like misbehaviour, let me know; it's changeable.)

All of the SecureConfig* classes can be used with or without encryption keys,
although you'll get a SecureConfigException('bad data or no encryption key') if
you try to parse a data structure (such as JSON) out of encrypted text.

Finally, in secureconfig is a class called SecureString, which is a subclass of the
string object. Its special function is to zero out the memory location of the string
payload. This class has its own section and explanation at the bottom.

SecureString must be considered HAZARDOUS MATERIALS and not implicitly trusted.
See below for why.



Installation and Requirements
-----------------------------

To install secureconfig, you'll need to have the development libraries for libffi
and libssl installed on your system.  On ubuntu, therefore, you'd do this::

   sudo apt-get install libffi-dev libssl-dev

Beyond this requirement, most users will find they can install secureconfig via pip:

   pip install secureconfig 

The following requirements form the backbone of secureconfig::

   cryptography
   configparser
   cffi
   pycparser

If you have any problems installing these requirements, please let us know as a
github issue at https://github.com/nthmost/python-secureconfig

SecureConfigParser
------------------

SecureConfigParser is a subclass of the configparser module's ConfigParser class.

The difference is that, when instantiated via one of the standardized cryptkeeper 
classmethods (see above) so that a private key is supplied, SecureConfigParser
detects encrypted entries and decrypts them when demanded (i.e. when .get is used).

So, unlike SecureJson, this class encrypts and decrypts single values rather than
entire files.

All of the usual ConfigParser methods are available.

In addition, you can set new values into the config to be encrypted by supplying
`encrypt=True` as an argument to the .set method. See an example of this below.


.. code-block:: python

    from secureconfig import SecureConfigParser

    # starting with an ini file that has unencrypted entries:
    configpath = '/etc/app/config.ini'

    key_env = 'SCP_INI_KEY'

    scfg = SecureConfigParser.from_env('SCP_INI_KEY')
    scfg.read(configpath)

    username = scfg.get('credentials', 'username')
    password = scfg.get('credentials', 'password')
        
    connection = GetSomeConnection(username, password)

    # IMPORTANT: supply encrypt=True to encrypt values.
    scfg.set('credentials', 'password', 'better_password', encrypt=True)
    
    fh=open('/path/to/new_scfp.ini', 'w')
    scfg.write(fh)
    fh.close()


SecureJson
----------

SecureJson is a very simple wrapper around JSON data. It decrypts whole files
(or whole strings) and can encrypt new configurations as well.

Use one of the cryptkeeper classmethods above to instantiate with a key. SecureJson will 
happily process plaintext data as well if no key is supplied.

SecureJson is a subclass of SecureConfig (see below), and as such, as some
ConfigParser-like operations included.


Basic usage (CHANGED SINCE 0.1.0):

.. code-block:: python

    from secureconfig import SecureJson

    configpath = '/etc/app/config.json.enc'

    config = SecureJson.from_file('.keys/aes_key', filepath=configpath)

    username = config.get('credentials', 'username')
    password = SecureString(config.get('credentials', 'password'))

    connection = GetSomeConnection(username, password)

    # SecureString overwrites its string data with zeroes upon garbage collection.
    del(password)
    
    # set a new password 
    config.set('credentials', 'password', 'better_password')
    
    fh=open('/path/to/config.json.enc', 'w')
    config.write(fh)
    fh.close()



SecureConfig
------------

WARNING: 

The way SecureConfig reads data back is via literal_eval. This approach may not
be without its concerns, so please do not use this class to work with data you 
do not explicitly trust.

The lowly SecureConfig class's lot in life is to be subclassed by other objects.
But it can still be somewhat useful.

SecureConfig stores data in serialized dictionaries, which are then encrypted
as a whole and stored as an undecipherable blob of information. The data can only
be read and recovered by supplying the private key that it was encrypted with.

SecureConfig provides a .cfg dictionary for raw access.  It also provides many ConfigParser
style interactions (see class docstring), including .get and .set methods.  This works as
long as your data is at least 2-dimensional.  

You can still use SecureConfig with 1-dimensional data (i.e. flat dictionary of key=value
pairs); you just can't use the ConfigParser style interactions. 

Below is demonstrated the non-ConfigParser style of interacting with SecureConfig data.

Basic Usage (CHANGED SINCE 0.1.0):

.. code-block:: python

    from secureconfig import SecureConfig

    config = SecureConfig.from_file('.keys/aes_key', filepath='/path/to/serialized.enc')

    cfg = config.cfg

    username = cfg['username']
    password = cfg['password']

    connection = GetSomeConnection(username, password)


SecureString
------------

"RAM security is haaaard" --Noah Kantrowitz, https://twitter.com/kantrn/status/461654722558963712

SecureString is a subclass of the string object with one modification: when deleted
and garbage-collected by python, or when its .burn() function is called, which 
explicitly zeroes out the data.

Now this documentation must spend due time convincing you why it is not "secure".

Python generally tries to create references to 'payload' data in memory rather than
copy payloads whenever possible, but in those and other scenarios, you may wind up
having string data copied into other locations, and SecureString won't have any idea.

In a "tight" scenario, e.g. where SecureString could be used to receive the `password` 
and then immediately be "burned after reading", SecureString can be trusted to zero
out the string data completely.  Outside of these strict scenarios, a number of 
circumstances will create copies of your sensitive data in memory, such as 
concatenation of strings and use of the comparison operator on strings held in lists. 

You must also keep in mind that, even if you del(secure_string) and explicitly
run gc.collect(), your string will still be in memory if there are still references
to that string lying around in other objects.

Also, if your python program does not complete gracefully, garbage collection may
not run completely or at all, so SecureString memory will not be wiped.  If you want
to insert gc.collect() statements to proactively scrape these strings, that is an
option, but there can be performance drawbacks to aggressively running garbage 
collection operations.

Finally, different python interpreters handle memory differently, and SecureConfig 
hasn't yet been tested on more than just the standard python interpreter and the
ipython interpreter.

Given the above, SecureString cannot at this time be implicity trusted as
"secure", since so much depends upon how it's used.


Contributions
-------------

The home for SecureConfig is on github:
https://github.com/nthmost/secureconfig

If you'd like to contribute, please make sure you run the tests (I normally use pytest)
found in the tests/ directory.  I might merge fixes into master but I won't update pypi
with a new version unless ALL the tests pass.

If you want to contribute a novel feature, please file it as an issue in the github repo
so we can discuss it first!

Comments, critiques, and bug reports warmly welcomed.  Pull requests encouraged.

--Naomi Most, 2014-2020 and onward.

