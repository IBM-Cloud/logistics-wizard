from os import environ as env
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib


def compose_msg(email_file, format_args):
    """
    Compose an email message from the input HTML template, using
    the input args as format arguments

    :param email_file:  Filename of the HTML template.
    :param format_args: Formatting arguments for the email.
    """
    with open('server/emails/' + email_file, 'r') as html_template:
        return html_template.read().replace('\n', '').format(*format_args)


def send_email(to_addr, subject, message, msg_type):
    """
    Send an email from the SMTP settings defined in the environment
    variables.
    NOTE:  Expects that environment variables: SMTP_USER_NAME,
           SMTP_PASSWORD, SMTP_SERVER, and SMTP_SERVER_PORT are
           defined.

    :param to_addr:   The To address of the email.
    :param subject:   The Subject of the email.
    :param message:   The body of the email.
    :param msg_type:  The type of text in the body of the email.
    NOTE:  The file objects in the files parameter only need read and
           name attributes to work, we can create another interface
           to read files from the DB later.
    """
    username = env['SMTP_USER_NAME']
    password = env['SMTP_PASSWORD']

    # Construct Message from given args
    msg_text = MIMEText(message, msg_type)
    msg = MIMEMultipart(From=username, To=to_addr, Date=formatdate(localtime=True))
    msg['Subject'] = subject
    msg.attach(msg_text)

    # Send email
    server = smtplib.SMTP(env['SMTP_SERVER'], env['SMTP_SERVER_PORT'])
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(username, to_addr, msg.as_string())
    server.quit()
