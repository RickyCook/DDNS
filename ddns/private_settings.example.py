# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'thatpanda_ddns',
        'USER': 'thatpanda_ddns',
        'PASSWORD': '',
        'HOST': '/var/run/postgresql',
    }
}
