import code
import os
import sys


READLINE_SRC = """
# python startup file
import readline
import rlcompleter
import atexit
import os

completer = rlcompleter.Completer(globals())
readline.set_completer(completer.complete)

# tab completion
readline.parse_and_bind('Control-space: complete')
# history file
histfile = os.path.join(os.environ['HOME'], '.pythonhistory')
try:
    readline.read_history_file(histfile)
except IOError:
    pass

atexit.register(readline.write_history_file, histfile)
del os, histfile, readline, rlcompleter
"""

BANNER = """GSSAPI Interactive console
Python {ver} on {platform}
Type "help", "copyright", "credits" or "license" for more information about Python.

Functions for controlling the realm are available in `REALM`.
Session: {session}
Mechansim: {mech} ({driver}), Realm: {realm}, User: {user}, Host: {host}"""


class GSSAPIConsole(code.InteractiveConsole):
    def __init__(self, driver_cls, use_readline=True, realm_args={},
                 attach=None, *args, **kwargs):
        code.InteractiveConsole.__init__(self, *args, **kwargs)

        self._driver = driver_cls()
        if attach is None:
            self.realm = self._driver.create_realm(realm_args)
        else:
            self.realm = self._driver.attach_to_realm(attach, realm_args)

        self.locals['REALM'] = self.realm

        self.runsource('import gssapi')
        self.runsource('import gssapi.raw as gb')

        if use_readline:
            self._add_readline()

        if os.environ.get('LD_LIBRARY_PATH'):
            self.realm.env['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH']

    def stop(self):
        self._driver.destroy_realm(self.realm)

    def _add_readline(self):
        self.runsource(READLINE_SRC, '<readline setup>', 'exec')

    @property
    def session(self):
        return self._driver.identifier(self.realm)

    @property
    def banner_text(self):
        return BANNER.format(ver=sys.version, platform=sys.platform,
                             session=self.session,
                             mech=self._driver.MECH_NAME,
                             driver=self._driver.PROVIDER_NAME,
                             realm=self.realm.realm,
                             user=self.realm.user_princ,
                             host=self.realm.host_princ)

    def interact(self, banner=None):
        if banner is None:
            banner = self.banner_text

        # Python 2.7 uses old-style classes :-(
        code.InteractiveConsole.interact(self, banner)
