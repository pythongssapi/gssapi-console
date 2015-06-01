GSSAPI Console
==============

*GSSAPI Console* allows provides an easy way to test out Python applications
using GSSAPI in a self-contained environment.

By default, the console will set up a self-contained MIT krb5 environment.
However, other GSSAPI environments are planned.

Requirements
------------

* [python-gssapi](https://pypi.python.org/pypi/gssapi) >= 1.1.0
* The required components for the environment in used
  (for krb5, the full set of MIT krb5 executables are needed,
  including those required to set up a KDC).

Usage
-----

*[further information is available by running `gssapi-console.py --help`]*

The main executable of GSSAPI Console is `gssapi-console.py`.  The basic
invocation works just like launching `python` -- use `gssapi-console.py FILE`
to run a file in the established environment, or just run `gssapi-console.py`
or `gssapi-console.py -i` to get an interactive environment (the `-i` flag
can be used with a file, just like `python FILE -i`).

You can use `--realm-args key1=true,key2=false,...` to pass specific arguments
to the realm constructor (the set of such keys is driver-dependent), and
`--mech MECH_NAME` can be used to specify a different driver (currently
only `--mech krb5` will work).
