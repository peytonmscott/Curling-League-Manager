from Backend.identified_object import IdentifiedObject


class TeamMember(IdentifiedObject):
    # __init__(oid, name, email)
    def __init__(self, oid, _player_name, _player_email):
        super().__init__(oid)
        self._name = _player_name
        self._email = _player_email

    @property
    # name (prop), getname
    def name(self):
        return self._name

    @property
    # email (prop), getemail
    def email(self):
        return self._email

    @name.setter
    def name(self, prop):
        self._name = prop

    @email.setter
    def email(self, prop):
        self._email = prop

    def send_email(self, emailer, subject, message):
        emailer.send_plain_email([self.email], subject, message)

    # __str__() -- return a string like the following: "Name<Email>"
    def __str__(self):
        return str(self.name + "<" + self.email + ">")

        
        
    



