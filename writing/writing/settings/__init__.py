import socket
import os

if socket.gethostname()==os.environ.get('LOCAL_HOST'):
    from .dev import *
else:
    from .production import *
