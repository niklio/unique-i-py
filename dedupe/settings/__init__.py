import os

from .base import *

env = os.environ['HOST_ENV']
if env == 'development':
    from .development import *
elif env == 'production':
    from .production import *
else:
    print 'Unrecognized enviornment'