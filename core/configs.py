import os

from dotenv import load_dotenv

load_dotenv()

constance_additional_fieldsets = {
    'password_form': ['django.forms.fields.CharField', {
        'widget': 'django.forms.PasswordInput',
        'required': False
    }],

    'email_form': ['django.forms.fields.EmailField', {
        'widget': 'django.forms.EmailInput',
        'required': False
    }],


}

constance_config = {
    'DEBUG': (True, 'Enable debug', bool),
    'USE_DEBUG_TOOLBAR': (False, 'Enable debug toolbar', bool),

    'ACCESS_TOKEN_LIFETIME': (int(os.getenv('ACCESS_TOKEN_LIFETIME')), 'Access token lifetime (in hours)', int),
    'REFRESH_TOKEN_LIFETIME': (int(os.getenv('REFRESH_TOKEN_LIFETIME')), 'Refresh token lifetime (in days)', int),
    'SLIDING_TOKEN_LIFETIME': (int(os.getenv('SLIDING_TOKEN_LIFETIME')), 'Sliding token lifetime (in minutes)', int),
    'SLIDING_TOKEN_REFRESH_LIFETIME': (int(os.getenv('SLIDING_TOKEN_REFRESH_LIFETIME')), 'Sliding token refresh lifetime (in days)', int),

    'PAGE_SIZE': (40, 'Page size', int),

    'DJANGO_STATICFILES_DIRS': ('assets/', 'Directory to Django static files', str),
    'DJANGO_DATABASE': ('dev', 'Django database name', str),

    'CHANNEL_BACKEND': ('channels_redis.core.RedisChannelLayer', 'Channel backend', str),
    'CHANNEL_HOST': ('127.0.0.1', 'Channel host', str),
    'CHANNEL_PORT': (6379, 'Channel port', int),
}

constance_config_fieldsets = {
    'Debug': {
        'fields': ('DEBUG', 'USE_DEBUG_TOOLBAR'),
        'collapse': True,
    },

    'SimpleJWT': {
        'fields': ('ACCESS_TOKEN_LIFETIME', 'REFRESH_TOKEN_LIFETIME',
                   'SLIDING_TOKEN_LIFETIME', 'SLIDING_TOKEN_REFRESH_LIFETIME'),
        'collapse': True,
    },
    'REST': {
        'fields': ('PAGE_SIZE',),
        'collapse': True,
    },
    'Django': {
        'fields': ('DJANGO_STATICFILES_DIRS', 'DJANGO_DATABASE'),
        'collapse': True,
    },
    'Redis': {
        'fields': ('CHANNEL_BACKEND', 'CHANNEL_HOST', 'CHANNEL_PORT'),
        'collapse': True,
    },
}
