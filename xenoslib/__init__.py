import sys
import importlib.metadata

__version__ = importlib.metadata.version('xenoslib')

if sys.platform == 'win32':
    from .windows import *
    from .win_trayicon import *
else:
    from .linux import *
from .base import *
from .dev import *
from .dev import RestartWhenModified as RestartSelfIfUpdated  # deprecated class name
from .extend import *
