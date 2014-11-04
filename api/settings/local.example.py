import os
from api.settings import base

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uwk$zoh26l^nc!#02+ui2(5n+1w*agn=u-+v6yzend4fzry$)%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

CORS_ORIGIN_WHITELIST = (
    'localhost:8080',
)

ALLOWED_HOSTS = ['localhost']

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(base.BASE_DIR, '../../db.sqlite3'),
    }
}
