import inspect
import logging


flogger = logging.getLogger('emails_gdpr.file')
logger = logging.getLogger('emails_gdpr')


def starting():
    logger.info('Starting %s...' % inspect.stack()[1][3])


def finished():
    logger.info('...Finished %s' % inspect.stack()[1][3])


def outbox_found(f_path):
    logger.info('Found outbox at: %s' % f_path)


def email_found(email, outbox):
    logger.info('Found email address (%s) for %s' % (email, outbox))


def processing_msg(author, recipient):
    logger.info('Processing message (from: %s, to: %s).' % (author, recipient))


def email_dont_match():
    logger.info('Neither author nor recipients emails match any of your emails.')


def mailbox_results(mbox):
    flogger.info(str(mbox))
