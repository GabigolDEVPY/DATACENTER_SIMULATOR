INSTALLED_APPS = [
    "daphne",
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notify',
]


DATABASES = {

    "default": {

        "ENGINE":"django.db.backends.mysql",

        "NAME":"projeto",

        "USER":"root",

        "PASSWORD":"root",

        "HOST":"mysql",

        "PORT":"3306"
    }

}


STATIC_URL="/static/"

STATIC_ROOT=BASE_DIR/"static"

ASGI_APPLICATION="core.asgi.application"