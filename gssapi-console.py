#!/usr/bin/env python

# interactive console with easy access to krb5 test harness stuff

import argparse
import os
import sys
import copy

import pkg_resources as pkgres

from gssapi_console import GSSAPIConsole


parser = argparse.ArgumentParser(
    description='An interactive Python console with krb5 setup')
parser.add_argument('file', metavar='FILE', nargs='?',
                    help='a file to run', default=None)
parser.add_argument('-i', default=False, dest='force_interactive',
                    action='store_const', const=True,
                    help='Force interactive mode when running with a file')
parser.add_argument('--realm-args', default=None,
                    help='A comma-separated list of key=(true|false) values '
                         'to pass to the realm constructor')
parser.add_argument('--mech', default='krb5',
                    help='Which environment to setup up '
                         '(supports krb5 [default])')

PARSED_ARGS = parser.parse_args()

realm_args = {}
if PARSED_ARGS.realm_args:
    for arg in PARSED_ARGS.realm_args.split(','):
        key, raw_val = arg.split('=')
        realm_args[key] = (raw_val.lower() == 'true')

try:
    mech_cls_loader = next(
        pkgres.iter_entry_points('gssapi_console.drivers',
                                 name=PARSED_ARGS.mech))
except StopIteration:
    sys.exit('The %s environment is not supported by the '
             'GSSAPI console' % PARSED_ARGS.mech)

mech_cls = mech_cls_loader.load()
SAVED_ENV = None

try:
    # import the env
    SAVED_ENV = copy.deepcopy(os.environ)
    console = GSSAPIConsole(mech_cls, realm_args=realm_args)
    for k, v in console.realm.env.items():
        os.environ[k] = v

    INTER = True
    # run the interactive interpreter
    if PARSED_ARGS.file is not None:
        if not PARSED_ARGS.force_interactive:
            INTER = False

        with open(PARSED_ARGS.file) as src:
            console.runsource(src.read(), src.name, 'exec')

    if INTER:
        console.interact()

except (KeyboardInterrupt, EOFError):
    pass
finally:
    # restore the env
    if SAVED_ENV is not None:
        for k in copy.deepcopy(os.environ):
            if k in SAVED_ENV:
                os.environ[k] = SAVED_ENV[k]
            else:
                del os.environ[k]

    console.stop()
