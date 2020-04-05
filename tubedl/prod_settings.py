import os

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base_settings import *  # noqa: F403

DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()  # noqa: F405

if os.environ.get('ADMIN_NAME') and os.environ.get('ADMIN_EMAIL'):
    ADMINS = (
        (os.environ['ADMIN_NAME'], os.environ['ADMIN_EMAIL']),
    )
    MANAGERS = ADMINS

EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME', '')
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD', '')

# configure Sentry
SENTRY_PUBLIC_KEY = os.environ.get('SENTRY_PUBLIC_KEY')
SENTRY_PROJECT_ID = os.environ.get('SENTRY_PROJECT_ID')

if None not in [SENTRY_PUBLIC_KEY, SENTRY_PROJECT_ID]:
    dsn = f'https://{SENTRY_PUBLIC_KEY}@sentry.io/{SENTRY_PROJECT_ID}'
    sentry_sdk.init(dsn=dsn, integrations=[DjangoIntegration()])
