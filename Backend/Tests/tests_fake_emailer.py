class FakeEmailer:
    def __init__(self):
        self.recipients = None
        self.subject = None
        self.message = None

    def send_plain_email(self, recipients, subject, message):
        self.recipients = recipients
        self.subject = subject
        self.message = message
