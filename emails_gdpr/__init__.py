__author__ = """Damian P."""
__email__ = 'an0o0nyme@gmail.com'
__version__ = '1.0.6'

import logging.config

from emails_gdpr import settings

logging.config.dictConfig(settings.logging_config)
