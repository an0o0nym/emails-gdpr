import configparser
import mailbox
import os
import platform

from emails_gdpr import exc, imap_utf7, settings, logs, utils


class MailBox:
    def __init__(self, email):
        self.email = email
        self.emails_in = set()
        self.emails_out = set()
        self.domains_in = set()
        self.domains_out = set()

        self.emails_gdpr = set()
        self.domains_gdpr = set()

    def __repr__(self):
        return 'MailBox(%s)' % self.email

    def __str__(self):
        return self.build_str_emails() + self.build_str_domains()

    def add_outgoing(self, recipient_email):
        self.emails_out.add(recipient_email)
        self.domains_out.add(utils.extract_tld(recipient_email))

    def add_incoming(self, author_email):
        self.emails_in.add(author_email)
        self.domains_in.add(utils.extract_tld(author_email))

    def process(self):
        self.emails_gdpr = self.emails_in - self.emails_out
        self.domains_gdpr = self.domains_in - self.domains_out

    def build_str_emails(self):
        s = 'Emails to GDPR for %s:\n' % self.email
        if not self.emails_gdpr:
            return '%s No emails yet.\n' % s

        for email in self.emails_gdpr:
            s += '\t- %s\n' % email
        return s

    def build_str_domains(self):
        s = 'Domains to GDPR for %s:\n' % self.email
        if not self.domains_gdpr:
            return '%s No domains yet.\n' % s

        for domain in self.domains_gdpr:
            s += '\t- %s\n' % domain
        return s


def discover_config_dir():
    logs.starting()

    os_platform = platform.system()
    for os_name, config_dir in settings.PROFILE_DIRS.items():
        if not os_platform.lower() in os_name:
            continue

        path = os.path.expanduser(config_dir)
        ini_path = os.path.join(path, 'profiles.ini')
        if not os.path.exists(ini_path):
            continue
        logs.finished()
        return path

    raise exc.ConfigNotFound('No config directory found.')


def discover_profile_dir(config_dir):
    logs.starting()

    parser = configparser.ConfigParser()
    parser.read(os.path.join(config_dir, 'profiles.ini'))
    for section in parser.sections():
        if 'Profile' not in section:
            continue

        logs.finished()
        return os.path.join(config_dir, parser[section]['path'])

    raise exc.ProfileNotFound('No profiles found.')


def discover_my_emails(profile_dir):
    logs.starting()

    outboxes = []
    for root, dirs, files in os.walk(profile_dir):
        for f_path in files:
            if f_path.endswith(('.dat', '.msf')):
                continue

            f_path_decoded = imap_utf7.decode(f_path.encode())
            is_outbox = any(f_name in f_path_decoded
                            for f_name in settings.OUTBOX_FOLDERS)
            if not is_outbox:
                continue

            logs.outbox_found(f_path)
            outboxes.append(os.path.join(root, f_path))

    if not outboxes:
        raise exc.OutboxNotFound('No outbox folders found')

    emails = []
    for outbox in outboxes:
        try:
            _, msg = mailbox.mbox(outbox).popitem()
        except KeyError:
            # If outbox is empty
            continue

        email_n = utils.email_norm(msg['from'])
        if not email_n:
            continue

        logs.email_found(email_n, outbox)
        emails.append(email_n)

    logs.finished()
    return emails


def get_all_messages(db_path):
    logs.starting()

    sql = "SELECT DISTINCT c3author, c4recipients FROM messagesText_content"
    with utils.get_db_conn(db_path) as cur:
        cur.execute(sql)
        messages = cur.fetchall()

    logs.finished()
    return messages


def parse_recipients(recipients):
    if ',' in recipients:
        recipients = recipients.split(',')

    if isinstance(recipients, str):
        recipients = {recipients}

    result = set()
    for recipient in recipients:
        email_n = utils.email_norm(recipient.strip())
        if not email_n:
            continue
        result.add(email_n)
    return result


def generate_mailboxes(messages, my_emails):
    mailboxes = {my_email: MailBox(my_email) for my_email in my_emails}

    for message in messages:
        author = utils.email_norm(message['c3author'])
        if not author:
            continue

        for recipient in parse_recipients(message['c4recipients']):
            logs.processing_msg(author, recipient)
            if author in my_emails:
                mailboxes[author].add_outgoing(recipient)
                continue

            if recipient in my_emails:
                mailboxes[recipient].add_incoming(author)
                break
            logs.email_dont_match()

    logs.finished()
    return mailboxes


def main():
    config_dir = discover_config_dir()
    profile_dir = discover_profile_dir(config_dir)
    my_emails = discover_my_emails(profile_dir)

    with utils.make_db_copy(profile_dir) as db_path:
        messages = get_all_messages(db_path)

    mailboxes = generate_mailboxes(messages, my_emails)

    for mbox in mailboxes.values():
        mbox.process()
        logs.mailbox_results(mbox)


if __name__ == '__main__':
    main()
