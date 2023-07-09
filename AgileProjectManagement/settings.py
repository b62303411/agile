import os
import logging
# Set up logging
logging.basicConfig(level=logging.INFO)
logging.info('Loading settings...')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'AgileProjectManagement',
        'USER': '<your_postgres_user>',
        'PASSWORD': '<your_postgres_password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

ALLOWED_HOSTS = ['*']

logging.info('Settings loaded successfully.')