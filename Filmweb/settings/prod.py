from Filmweb.settings.base import *
import django_on_heroku
import django

# override base settings here
DEBUG = True
ALLOWED_HOSTS = ['localhost', '.herokuapp.com', ".filmwebscrapping.herokuapp.com", '127.0.0.1']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST': os.getenv('DATABASE_URL1'),
        'PORT': '5432',
    }
}
print(f"This is my TEMPLATES_DIRS: {DATABASES}")
# MEDIA_ROOT = os.path.join(BASE_DIR, 'my_media')
django.setup()
django_on_heroku.settings(locals())
