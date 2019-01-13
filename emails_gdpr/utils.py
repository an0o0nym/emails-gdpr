import os
import shutil
import sqlite3
import unicodedata
from contextlib import contextmanager

import tldextract
from cachetools import cached, LRUCache
from email_normalize import normalize as norm_email

cache = LRUCache(maxsize=500)
        

@cached(cache)
def email_norm(email):
    try:
        return norm_email(email, resolve=False)
    except ValueError:
        print('Error parsing email %s' % email)


@cached(cache)
def extract_tld(email):
    return tldextract.extract(email).registered_domain


def norm_path(path):
    return unicodedata.normalize('NFD', path)


@contextmanager
def get_db_conn(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        cur = conn.cursor()
        yield cur
    finally:
        cur.close()

    conn.close()


@contextmanager
def make_db_copy(profile_dir):
    db_path = os.path.join(profile_dir, 'global-messages-db.sqlite')
    db_copy_path = os.path.join(profile_dir, 'global-messages-db-copy.sqlite')
    shutil.copyfile(db_path, db_copy_path)

    try:
        yield db_copy_path
    finally:
        os.remove(db_copy_path)
