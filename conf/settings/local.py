from .base import *

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        "ENGINE": os.environ.get('LOCAL_DATABASE_ENGINE'),
        "NAME": os.environ.get('LOCAL_DATABASE_NAME'),
        "USER": os.environ.get('LOCAL_DATABASE_USER'),
        "PASSWORD": os.environ.get('LOCAL_DATABASE_PASSWORD'),
        "HOST": os.environ.get('LOCAL_DATABASE_HOST'),
        "PORT": os.environ.get('LOCAL_DATABASE_PORT'),
    }
}