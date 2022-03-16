import sys
if sys.platform == 'win32':
    from .windows import *
else:
    from .linux import *
from .base import *
from .dev import *
from .dev import RestartWhenModified as RestartSelfIfUpdated  # deprecated class name
from .extend import *
__version__ = '0.1.6.6'
