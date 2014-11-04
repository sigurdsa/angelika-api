from api.settings.base import *

try:
    from api.settings.local import *
except ImportError, e:
    detail = "Failed to import local settings. Check if you have local.py. If not, copy local.py.example to local.py"
    raise ImportError(detail)
