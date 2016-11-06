# coding: utf-8
""" Email Tamplate with UTF-8 Support.
Supported variables $name, $to_addr, $last_payment, $days_due
"""

SUBJECT = 'subject $name'
BODY = """\
Αβγδεέαά $name <$to_addr>

your last payment was made at $last_payment this means that as of today your
subscriptios is due for almost $days_due days.

"""
