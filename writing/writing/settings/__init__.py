import socket
import os

if socket.gethostname()==os.environ.get('LOCAL_HOST'):
    from .development import *
else:
    from .production import *
