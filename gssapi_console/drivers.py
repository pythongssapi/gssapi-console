import os
import sys


class GSSAPIConsoleDriver(object):
    MECH_NAME = ''
    PROVIDER_NAME = ''

    def create_realm(self, realm_args):
        return None

    def destroy_realm(self, realm):
        pass

    def attach_to_realm(self, identifier, realm_args={}):
        pass

    def identifier(self, realm):
        return None


class Krb5Console(GSSAPIConsoleDriver):
    MECH_NAME = 'krb5'
    PROVIDER_NAME = 'MIT Kerberos 5'

    def __init__(self):
        __import__('k5test')
        self._k5test = sys.modules['k5test']

    def create_realm(self, realm_args):
        return self._k5test.K5Realm(**realm_args)

    def destroy_realm(self, realm):
        realm.stop()

    def attach_to_realm(self, identifier, realm_args={}):
        return self._k5test.K5Realm(existing=identifier, **realm_args)

    def identifier(self, realm):
        return realm.tmpdir
