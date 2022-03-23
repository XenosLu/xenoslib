import sys

if sys.platform == 'win32':
    from .windows import *
    from .win_trayicon import *
else:
    from .linux import *
from .base import *
from .dev import *
from .dev import RestartWhenModified as RestartSelfIfUpdated  # deprecated class name countdown 2
from .extend import *
