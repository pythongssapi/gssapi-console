import pkg_resources as pkgres
import copy
import os

class GSSAPIYalptDriver(object):
    DRIVER_NAME = "GSSAPI"
    BANNER = """Functions for controlling the realm are available in `REALM`.
Mechansim: {mech} ({driver}), Realm: {realm}, User: {user}, Host: {host}"""

    def __init__(self, args=None):
        self._realm_args = {}

        if args is None:
            driver = 'krb5'
        else:
            args_parts = args.split(';')
            driver = args_parts[0]

            if len(args_parts) > 1:
                realm_args_raw = args_parts[1]
                for arg in realm_args_raw.split(','):
                    key, raw_val = arg.split('=')
                    self._realm_args[key] = (raw_val.lower() == 'true')

        try:
            driver_loader = next(
                pkgres.iter_entry_points('gssapi_console.drivers',
                                         name=driver))
        except StopIteration:
            raise ValueError("No such GSSAPI Console driver %s." % driver)

        self._driver = driver_loader.load()()

        self._saved_env = None
        self._realm = None

    def setup(self):
        self._saved_env = copy.deepcopy(os.environ)
        self._realm = self._driver.create_realm(self._realm_args)
        for k, v in self._realm.env.items():
            os.environ[k] = v

        return {'REALM': self._realm}

    def teardown(self):
        if self._saved_env is not None:
            for k in copy.deepcopy(os.environ):
                if k in self._saved_env:
                    os.environ[k] = self._saved_env[k]
                else:
                    del os.environ[k]

            self._saved_env = None

        self._driver.destroy_realm(self._realm)

    @property
    def banner(self):
        return self.BANNER.format(mech=self._driver.MECH_NAME,
                                  driver=self._driver.PROVIDER_NAME,
                                  realm=self._realm.realm,
                                  user=self._realm.user_princ,
                                  host=self._realm.host_princ)

