import sys

from .version import __version__  # noqa

if sys.platform == 'win32':
    from .windows import *  # noqa
    from .win_trayicon import *  # noqa
else:
    from .linux import *  # noqa
from .base import *  # noqa
from .dev import *  # noqa
from .dev import (  # noqa
    RestartWhenModified as RestartSelfIfUpdated,
)  # deprecated class name countdown 1

