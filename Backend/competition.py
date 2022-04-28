from sys import settrace
from identified_object import IdentifiedObject


class Competition(IdentifiedObject):

    def __init__(self, oid, teams_competing, location, date_time, ):
        super().__init__(oid)
        self._teams_competing = teams_competing
        self.date_time = date_time
        self.location = location

    @property
    def teams_competing(self):
        return self._teams_competing

    @teams_competing.setter
    def teams_competing(self, prop):
        teams_competing = prop
