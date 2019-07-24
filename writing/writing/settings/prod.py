from .base import *

print('Running production settings.')
DEBUG = False

try:
    from .local import *
except ImportError:
    pass
