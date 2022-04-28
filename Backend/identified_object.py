class IdentifiedObject:
    # Initializes an object with an OID (and sets current ID one higher)
    def __init__(self, oid):
        self._oid = oid

    @property
    def oid(self):
        return self._oid

    def __eq__(self, other):
        return self._oid == other.oid

    def __hash__(self):
        return hash(self._oid)


class DuplicateOid(Exception):
    def __init__(self, message, oid):
        self.message = message
        self.oid = oid


class DuplicateEmail(Exception):
    def __init__(self, message, oid):
        self.message = message
        self.oid = oid
