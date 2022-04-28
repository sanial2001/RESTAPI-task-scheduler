import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import settings

username = f"{settings.mail_username}"
password = f"{settings.mail_password}"


def send_mail(text="Email Body", subject="Hello World", from_email=f'Sanial <{username}>', to_emails=None, html=None):
    print(to_emails)
    assert isinstance(to_emails, list)

    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject

    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)
    if html != None:
        html_part = MIMEText(html, 'html')
        msg.attach(html_part)

    msg_string = msg.as_string()

    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg_string)
    server.quit()


'''
    send_mail(text="Email Body", subject="Email testing", from_email=f'Sanial <{username}>',
              to_emails=['sanial2001@gmail.com', 'sanial.das@iiitg.ac.in'], html='')
'''