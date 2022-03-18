import sys
if sys.platform == 'win32':
    from .windows import *
    from .win_trayicon import *
else:
    from .linux import *
from .base import *
from .dev import *
from .dev import RestartWhenModified as RestartSelfIfUpdated  # deprecated class name
from .extend import *
__version__ = '0.1.9.2'
