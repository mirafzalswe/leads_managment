import ssl
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend

class CustomEmailBackend(SMTPBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE 