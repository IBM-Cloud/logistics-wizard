from os import environ as env
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib


def compose_welcome_msg(demo_guid, user):
    return """\
    <html>
        <head></head>
        <body>
            <p>
                Congratulations, you have created a new session for the Logistics Wizard demo!
                You can access your demo session at the following URL:<br>
                https://logistics-wizard.mybluemix.net/demo/""" + demo_guid + """
            </p>
            <p>
                If you want to take the demo beyond the UI, you may find the following information useful:
            </p>
            <p>
                <b>GUID</b>: """ + demo_guid + """<br>
                <b>Default Username</b>: """ + user.get('username') + """<br>
                <b>Default User ID</b>: """ + str(user.get('id')) + """<br>
            </p>
            <p>
                The Logistics Wizard Controller API is entirely open so that anyone is able to
                leverage it programmatically or create their own UI. Check out the
                <a href=http://editor.swagger.io/#/?import=https://raw.githubusercontent.com/
                IBM-Bluemix/logistics-wizard/master/swagger.yaml>Swagger API Spec</a> to better
                understand the methods available to you or take advantage of our
                <a href="https://app.getpostman.com/run-collection/b39a8c0ce27371fbd972#?env%5BLW_Prod%
                5D=W3sia2V5IjoiZXJwX2hvc3QiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2dpc3RpY3Mtd2l6YXJkLWVycC5teWJsdWVt
                aXgubmV0LyIsInR5cGUiOiJ0ZXh0IiwiZW5hYmxlZCI6dHJ1ZSwiaG92ZXJlZCI6ZmFsc2V9LHsia2V5IjoiY29
                udHJvbGxlcl9ob3N0IiwidmFsdWUiOiJodHRwczovL2xvZ2lzdGljcy13aXphcmQubXlibHVlbWl4Lm5ldCIsIn
                R5cGUiOiJ0ZXh0IiwiZW5hYmxlZCI6dHJ1ZSwiaG92ZXJlZCI6ZmFsc2V9XQ==">Postman collection</a>
                to help you get started with the REST interface.
            </p>
            <p>
                Thanks,<br>
                The Logistics Wizard Team
            </p>
        </body>
    </html>
    """


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
