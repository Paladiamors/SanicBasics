import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from settingsManager import get_settings


def mail(subject, text, to, cc=None, bcc=None, attachments=None,
         mode="html", username=None, pw=None):
    """
    subject = subject of mail
    text = text of body
    to = recipient, defaults to what is in settings
    attach = attachments to send
    """

    settings = get_settings()
    server = settings.get_setting("mail/server")

    username = username or settings.get_setting("mail/default_user")
    pw = pw or settings.get_setting(f"mail/users/{username}")

    if not username or not pw:
        raise RuntimeError("No crednetials specified")

    msg = MIMEMultipart()

    to = [to] if isinstance(to, str) else [to]
    msg['From'] = username
    msg['To'] = ",".join(to)
    if cc:
        msg['Cc'] = ",".join(cc)
        to.append(cc)
    if bcc:
        msg['Bcc'] = ",".bcc
        to.append(bcc)

    msg['Subject'] = subject

    if mode == "html":
        msg.attach(MIMEText(text, "html"))
    else:
        msg.attach(MIMEText(text, "plain"))

    if attachments:
        for attach in attachments:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(attach, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % os.path.basename(attach))
            msg.attach(part)

    mailServer = smtplib.SMTP(server, 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(username, pw)
    mailServer.sendmail(username, ",".join(to), msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()


def stocknpv_mail():
    html = """\
    <html>
      <head></head>
      <body>
        <p>Welcome to StockNPV!<br>
           Glad to have you onboard.<br>
           To access the site please use this <a href="https://www.stocknpv.com">link</a>.
        </p>
      </body>
    </html>
    """

    to = "justinyho@gmail.com"
    subject = "Welcome to StockNPV your account has been created"
    username = "service@stocknpv.com"
    mail(subject, html, to, username=username)


def spherex_mail():
    html = """\
    <html>
      <head></head>
      <body>
        <p>Welcome to spherex!<br>
           Glad to have you onboard.<br>
           To access the site please use this <a href="https://www.spherex.dev">link</a>.
        </p>
      </body>
    </html>
    """

    to = "justinyho@gmail.com"
    subject = "Welcome to spherex your account has been created"
    username = "info@spherex.dev"
    mail(subject, html, to, username=username)


if __name__ == "__main__":

    spherex_mail()
