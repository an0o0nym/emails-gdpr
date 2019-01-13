import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


PROFILE_DIRS = {
    'windows_old': '~\\Application Data\\Thunderbird\\Profiles\\',
    'windows': '~\\AppData\\Roaming\\Thunderbird\\Profiles\\',
    'linux': '~/.thunderbird/',
    'linux_other': '~/.mozilla-thunderbird/',
    'osx': '~/Library/Thunderbird/Profiles/',
}


OUTBOX_FOLDERS = ['Sent', 'Wysłane']


logging_config = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        'default': {
            'format': '[{levelname}] [{asctime}]: {message}',
            'style': '{'
        },
        'plain': {
            'format': '{message}',
            'style': '{'
        }
    },
    handlers={
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': logging.DEBUG
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'plain',
            'level': logging.INFO,
            'filename': os.path.join(BASE_DIR, 'info.log'),
            'mode': 'w',
        },
    },
    loggers={
        'emails_gdpr': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'emails_gdpr.file': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        }
    },
)
