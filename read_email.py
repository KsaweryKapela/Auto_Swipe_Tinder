import email
import email.parser
import email.policy
import imaplib
import re
import time
import os
from dotenv import load_dotenv


SMS_FRAGMENT = "do Tindera to"
EMAIL_FRAGMENT = "YOUR CODE IS"

load_dotenv()
GMAIL_USERNAME = os.getenv("my_email")
GMAIL_PASSWORD = os.getenv("gmail_password")
HOST = 'imap.gmail.com'


def get_code_from_mail():
    mail = imaplib.IMAP4_SSL(HOST)
    mail.login(GMAIL_USERNAME, GMAIL_PASSWORD)

    _, search_data = mail.search(None, 'ALL')
    mail.select('INBOX')
    mail_list = search_data[0].split()
    tinder_message = mail_list[-1]
    _, data = mail.fetch(tinder_message, '(RFC822)')
    _, b = data[0]
    email_message = str(email.message_from_bytes(b))

    if EMAIL_FRAGMENT in email_message:
        m = re.search(f"{EMAIL_FRAGMENT} (\w+)", email_message)
        code = (m.groups())
        return code[0]
    else:
        time.sleep(3)


def get_code_from_sms():
    mail = imaplib.IMAP4_SSL(HOST)
    mail.login(GMAIL_USERNAME, GMAIL_PASSWORD)

    while True:
        mail.select('INBOX')
        _, search_data = mail.search(None, 'ALL')
        mail_list = search_data[0].split()
        tinder_message = mail_list[-1]
        _, data = mail.fetch(tinder_message, '(RFC822)')
        msg = email.message_from_bytes(data[0][1], policy=email.policy.default)
        body = ""

        for part in msg.walk():
            charset = part.get_content_charset()
            if part.get_content_type() == "text/plain":
                partStr = part.get_payload(decode=True)
                body += partStr.decode(charset)

        if SMS_FRAGMENT in body:
            m = re.search(f"{SMS_FRAGMENT} (\w+)", body)
            code = (m.groups())
            return str(code[0])
        else:
            time.sleep(4)
