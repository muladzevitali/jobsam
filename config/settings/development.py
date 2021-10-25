from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'media/database/db.sqlite3',
    }
}
