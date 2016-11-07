# coding: utf-8
"""Config file example. Rename to config.py"""

EMAIL_METHOD = 'smtp' #smtp, sendmail, none
EMAIL_FROM = 'user@example.com'

SMTP_SERVER = 'smtp.example.com:587'
SMTP_SECURETY = 'starttls' #starttls, none

SMTP_AUTH = True #True, False
SMTP_USERNAME = 'user@example.com'
SMTP_PASSWORD = ''

INTERVAL_DAYS = 1

FILENAME = 'members.csv'
