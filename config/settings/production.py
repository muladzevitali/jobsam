from src import config

DEBUG = False

ALLOWED_HOSTS = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': config.postgres_config.host,
        'PORT': config.postgres_config.port,
        'NAME': config.postgres_config.db,
        'USER': config.postgres_config.user,
        'PASSWORD': config.postgres_config.password,
    }
}
