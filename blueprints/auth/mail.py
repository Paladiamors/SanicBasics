from utils.mail import mail
from settingsManager import get_settings


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

    stocknpv_mail()
