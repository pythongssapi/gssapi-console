GSSAPI Console
==============

[![PyPI version](https://badge.fury.io/py/gssapi_console.svg)](https://badge.fury.io/py/gssapi_console)
[![GitHub version](https://badge.fury.io/gh/pythongssapi%2Fgssapi-console.svg)](https://badge.fury.io/gh/pythongssapi%2Fgssapi-console)

*GSSAPI Console* allows provides an easy way to test out Python applications
using GSSAPI in a self-contained environment.

By default, the console will set up a self-contained MIT krb5 environment.
However, other GSSAPI environments are planned.

Requirements
------------

* [python-gssapi](https://pypi.python.org/pypi/gssapi) >= 1.1.0
* Requirements for the environment used (for example, the default environment is
  MIT krb5, which uses the [k5test](https://pypi.python.org/pypi/k5test))

Usage
-----

*further information is available by running `gssapi-console.py --help`*

The main executable of GSSAPI Console is `gssapi-console.py`.  The basic
invocation works just like launching `python` -- use `gssapi-console.py FILE`
to run a file in the established environment, or just run `gssapi-console.py`
or `gssapi-console.py -i` to get an interactive environment (the `-i` flag
can be used with a file, just like `python FILE -i`).

There are several additional flags that may be passed to `gssapi-console.py`:

* `--realm-args key1=true,key2=false,...` can be used to pass specific arguments
  to the realm constructor (the set of such keys is driver-dependent)
* `--mech MECH_NAME` can be used to specify a different driver (currently, only
  `--mech krb5` will work)
* `-a IDENTIFIER, --attach IDENTIFIER` may be used to "attach" a new GSSAPI Console
  session to an environment set up by an existing GSSAPI Console session.  The identifier
  will be noted at the top of the existing GSSAPI Console session as `Session: IDENTIFIER`.
* `-v, --verbose` may be used to increase the verbosity of the logging level (generally to
  gain more details on what the driver is doing to set up the realm).

Additional GSSAPI Console drivers may be introduced using the `gssapi_console.drivers`
setuptools entry point.  They should follow the `gssapi_console.drivers.GSSAPIConsoleDriver`
class.

GSSAPI Console provides a [YALPT](https://pypi.python.org/pypi/yalpt) environment driver for
writing tutorials and literate python files involving GSSAPI.  You can use it by passing
`-e gssapi` to YALPT (it will use the default GSSAPI Console driver in this case).
