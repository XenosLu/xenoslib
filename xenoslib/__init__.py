import sys

from .about import __version__  # noqa

if sys.platform == 'win32':
    from .windows import *  # noqa
    from .win_trayicon import *  # noqa
else:
    from .linux import *  # noqa
from .base import *  # noqa
