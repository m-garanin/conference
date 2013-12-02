DATABASES = {
	'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'NAME': 'test_conference',
        'OPTIONS':  {
                        'autocommit': True        
                    }
		}
	}

MEDIA_ROOT = '/var/db/conference/'
MEDIA_URL = '/storage/'

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "25"
EMAIL_HOST_USER = "support@broadcast-online.ru"
EMAIL_HOST_PASSWORD = "support279"
EMAIL_USE_TLS = "True"

LOGIN_REDIRECT_URL = '/account/'

AUTHENTICATION_BACKENDS = (
    'app.backend.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)

