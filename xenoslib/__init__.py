import sys

if sys.platform == 'win32':
    from .windows import *  # noqa
    from .win_trayicon import *  # noqa
else:
    from .linux import *  # noqa
from .base import *  # noqa
from .dev import *  # noqa
from .dev import RestartWhenModified as RestartSelfIfUpdated  # deprecated class name countdown 2  # noqa
from .extend import *  # noqa
