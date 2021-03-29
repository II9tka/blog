import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'l4#264s9wff-8lxbq&7p*#-sqrnbw-vj8*a@t^x+*)qe26f8_3'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
    'channels',
    'drf_yasg',
    'colorfield',
    'versatileimagefield',
    'taggit',
    'taggit_serializer',
    'phonenumber_field',
    'phone_login',

    'backend.account',
    'backend.filer',
    'backend.article',
    'backend.chat'
]

ASGI_APPLICATION = "blog_main.asgi.application"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog_main.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# REST default

REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework.authentication.BasicAuthentication',
    #     'rest_framework.authentication.TokenAuthentication',
    # ),
    'DATETIME_FORMAT': "%d.%m.%Y %H:%M",
    'DATE_FORMAT': "%d.%m.%Y",
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50
}

# Auth

AUTH_USER_MODEL = 'account.Account'

# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
#     'phone_login.backends.phone_backend.PhoneBackend',
# ]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False
# USE_TZ = True

# Static settings

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Media settings

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Phone login settings

SENDSMS_FROM_NUMBER = "+79006506624"

# Elastic search dsl

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}

# Django channels

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_URL = 'redis://%s' % REDIS_HOST

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
            'capacity': 300
        },
    },
}

# Logger

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': 'debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}

# Versatile image field

VERSATILEIMAGEFIELD_SETTINGS = {
    'cache_length': 2592000,
    'cache_name': 'versatileimagefield_cache',
    'jpeg_resize_quality': 70,
    'sized_directory_name': '__sized__',
    'filtered_directory_name': '__filtered__',
    'placeholder_directory_name': '__placeholder__',
    'create_images_on_demand': True,
    'image_key_post_processor': None,
    'progressive_jpeg': False
}

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'public_account_image': [
        ('full_size', 'url'),
        ('medium_square_crop', 'crop__400x400'),
    ],
    'private_account_image': [
        ('medium_square_crop', 'crop__400x400'),
    ],
    'article_cover': [
        ('full_size', 'url'),
        ('medium_square_crop', 'crop__400x400'),
    ]
}
