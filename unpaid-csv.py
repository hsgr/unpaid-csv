from csv import reader
from datetime import date, datetime
from string import Template
from email_template import subject_, body_
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
from config import *

today = date.today()

def send_email(to, subject, body):
    msg = MIMEText(body.encode('utf-8'), _charset='utf-8')
    msg['Subject'] = Header(subject, "utf-8")
    msg['From'] = smtp_from
    msg['To'] = to
 
    server = SMTP(smtp_server)
    server.starttls()
    server.login(smtp_username, smtp_password)
    problems = server.sendmail(smtp_from, [to], msg.as_string())
    server.quit()

def subscription_due(last_payment):
    passed_days = (today - last_payment).days
    if (passed_days > interval_days):
        return (passed_days - interval_days)

def mail_loop(members):
    for member in members:
        last_payment = datetime.strptime(member[2], "%Y-%m-%d").date()
        days_due = subscription_due(last_payment)
        if days_due:
            name = member[0]
            to = member[1]
            subject = Template(subject_).substitute(locals())
            body = Template(body_).substitute(locals())
            send_email(to, subject, body)
            print (to + subject + body)

with open(filename, 'rt') as csvfile:
    members = reader(csvfile, delimiter=',')
    mail_loop(members)
