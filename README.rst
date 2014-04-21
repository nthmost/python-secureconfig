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
    Json (see SecureJson) -- whole-file encryption only.
    serialized dictionaries (see SecureConfig) -- whole-file encryption only.


Please let me know if you want to see another type supported.


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
ways of encrypting as well.

That's why secureconfig (as of 0.0.3) supports writing new config files.
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

This library can be found at https://bitbucket.org/nthmost/python-secureconfig 

Contributions and code critiques are warmly welcomed.


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
currently exists or not.  If this place is not writeable, you'll get the usual
error for that operation (OSError for files, KeyError for environment variables).

If CryptKeeper classes are instantiated without a key argument, they will generate
a key automatically for you.

Another way to generate a new key is to use the CryptKeeper classmethod `.generate_key()`.

All of the SecureConfig* classes can be used with or without encryption keys,
although you'll get a SecureConfigException('bad data or no encryption key') if
you try to parse a data structure (such as JSON) out of encrypted text.


SecureJson
----------

Basic usage (CHANGED SINCE 0.0.3):

.. code-block:: python

    from secureconfig import SecureJson, SecureString

    configpath = '/etc/app/config.json.enc'

    config = SecureJson.from_file('.keys/aes_key', filepath=configpath)

    username = config.get('credentials', 'username')
    password = SecureString(config.get('credentials', 'password'))

    connection = GetSomeConnection(username, password)

    # SecureString overwrites its string data with zeroes upon garbage collection.
    del(password)



SecureConfigParser
------------------

NEW IN 0.0.3:

.. code-block:: python

    from secureconfig import SecureConfigParser, SecureString

    # starting with an ini file that has unencrypted entries:
    configpath = '/etc/app/config.ini'

    key_env = 'SCP_INI_KEY'

    scfg = SecureConfigParser.from_env('SCP_INI_KEY')
    scfg.read(configpath)



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

SecureConfig provides a .cfg dictionary for raw access.  It also provides 
.get and .set methods, mimicking ConfigParser in its interface (this works as long 
as your data is exactly 2 levels deep).

Basic Usage (CHANGED SINCE 0.0.3):

.. code-block:: python

    from secureconfig import SecureConfig, SecureString

    config = SecureJson.from_file('.keys/aes_key')

    username = config.get('credentials', 'username')
    password = SecureString(config.get('credentials', 'password'))










Future
------

Planned features include::

- more automated-deployment-oriented utils
- asymmetric key deployments (e.g. RSA public key encryption)


CONTACT
-------

Look for @nthmost on Twitter if you're interested and would like to contribute!
Comments and critiques warmly welcomed.

--Naomi Most, spring 2014.

