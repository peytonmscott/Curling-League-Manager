import yagmail

class emailer:
    def __init__(self,email_id,password):
        yagmail.register(email_id, password)

    def login(self,email_id):
        self.instance=yagmail.SMTP(email_id)

    def send_plain_email(self,reciepent_list,subject,message):
        self.instance.send(reciepent_list,subject, message)


