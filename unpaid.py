#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Unpaid CSV.
A script for Hackerspace.gr to remind members of their late subscription fees.
"""

#    Copyright (C) 2016  Sotirios Vrachas <sotirio@vrachas.net>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from csv import reader
from datetime import date, datetime
from string import Template
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
from email_template import SUBJECT, BODY
from config import SMTP_FROM, SMTP_SERVER, SMTP_USERNAME, \
    SMTP_PASSWORD, INTERVAL_DAYS, FILENAME

TODAY = date.today()


def send_email(to_addr, subject, body):
    """Sends Email"""
    msg = MIMEText(body.encode('utf-8'), _charset='utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = SMTP_FROM
    msg['To'] = to_addr

    server = SMTP(SMTP_SERVER)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.sendmail(SMTP_FROM, [to_addr], msg.as_string())
    server.quit()


def subscription_due(last_paid):
    """Check if fees are due"""
    passed_days = (TODAY - last_paid).days
    if passed_days > INTERVAL_DAYS:
        return passed_days - INTERVAL_DAYS


def mail_loop(members):
    """Loop over members. Calls send_email if fees are due"""
    for member in members:
        last_paid = datetime.strptime(member[2], '%Y-%m-%d').date()
        days_due = subscription_due(last_paid)
        if days_due:
            name = member[0]
            to_addr = member[1]
            subject = Template(SUBJECT).substitute(name, to_addr, days_due, last_paid)
            body = Template(BODY).substitute(name, to_addr, days_due, last_paid)
            send_email(to_addr, subject, body)


with open(FILENAME, 'rt') as csvfile:
    MEMBERS = reader(csvfile, delimiter=',')
    mail_loop(MEMBERS)
