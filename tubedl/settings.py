import os

if os.environ.get('PRODUCTION'):
    from prod_settings import *  # noqa
else:
    from dev_settings import *  # noqa
