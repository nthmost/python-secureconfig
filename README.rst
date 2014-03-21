*******************
python-secureconfig
*******************

by Naomi Most (@nthmost)

A simple solution to the often annoying problem of protecting config files.

secureconfig makes keeping your secrets secure on servers and source control 
repositories easy by restricting your choices on the matter, defaulting to 
a "medium paranoia" set of operations.

Those choices, specifically::

 * use AES-256 (so, symmetric enc only, for the moment)
 * 


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

Of course, some setup is required before decryption can take place. A file
must be encrypted first, using keys that must be generated somewhere along
the line.

That's why secureconfig contains automated deployment utilities to assist 
in (for example) writing that fabfile.py in your repo directory. 


How secureconfig Works
----------------------

At its core, secureconfig simply subclasses the configuration mechanisms we 
all know and love, and wraps certain operations (read-from-file and/or 
read-and-interpolate) in a decryption layer.

This library bases its operations on keyczar, a multi-language encryption key 
management tool created in a collaboration between an MIT student and a Google 
employee, and it defaults to using 256-bit AES encryption.

As such, the operation of secureconfig involves storing keys in files. (Work is
currently being done on storing keys securely in environment variables.)

secureconfig wants you to store your keys in places protected by your operating
system.  If you let secureconfig create directories for storing your keys, they
will be created with restrictive (chmod 0700) permissions.

secureconfig aspires to being more versatile, but right now the things you can
do with it are as follows::

    * automate the secure creation, storage, and deployment of encryption
    keys, particularly in conjunction with Fabric (see secureconfig.utils)

    * encrypt whole config files in JSON and abstract away the process of decrypting
    and loading the configuration into a dictionary (see secureconfig.securejson)

    * completely zero-out the memory location where passwords and other sensitive
    information was stored in memory during the usage of credentials. 
    (see secureconfig.zeromem)


Basic usage::

    from secureconfig import SecureJson, zeromem

    # keep keyloc locked down! 
    # best is user directory + dot-file subdirectory w/ chmod 700
    keyloc = '/path/to/keys' 

    configpath = '/etc/app/config.json.enc'

    config = SecureJson(configpath, keyloc)

    username = config.get('credentials', 'username')
    password = config.get('credentials', 'password')

    connection = GetSomeConnection(username, password)

    zeromem(username)
    zeromem(password)



Future
------

Planned features include::

* SecureConfigParser (ConfigParser subclass supporting line-based encrypted variables)
* running in "paranoid mode" (e.g. refusing to use keys not stored in locked-down locations)
* more backgrounded usage of zeromem to prevent memory dump attacks.
* more automated-deployment-oriented utils
* asymmetric key deployments (e.g. DSA public key encryption)

There is currently no support for writing config files (as ConfigParser lets
you do), but that might be on the horizon.


CONTACT
-------

Look for @nthmost on Twitter if you're interested and would like to contribute!

