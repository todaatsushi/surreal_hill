import os
from dotenv import load_dotenv

load_dotenv('.env')

SECRET_KEY=os.environ.get('SECRET_KEY')
ALLOWED_HOSTS=[os.environ.get('CUSTOM_DOMAIN')]

from .base import *

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': os.environ.get('DB_NAME'),
		'USER': os.environ.get('DB_USER'),
		'PASSWORD': os.environ.get('DB_PASSWORD'),
		'HOST': os.environ.get('DB_HOST')
	}
}

