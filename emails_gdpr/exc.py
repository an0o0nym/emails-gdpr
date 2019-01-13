class GDPREmails(Exception):
    pass


class ConfigNotFound(GDPREmails):
    """ Exception raises when no profiles.ini directory is found."""
    pass


class ProfileNotFound(GDPREmails):
    """ Exception raises when no profiles are defined in profiles.ini file."""
    pass


class OutboxNotFound(GDPREmails):
    """
    Exception raises when no outbox folders containing pre-defined names
    are found in a profile directory.
    """
    pass
