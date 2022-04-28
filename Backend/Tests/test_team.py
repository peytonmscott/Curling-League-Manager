from team import Team
from team_member import TeamMember
import unittest

from tests_fake_emailer import FakeEmailer


class TeamTests(unittest.TestCase):
    def test_create(self):
        name = "Curl Jam"
        oid = 10
        t = Team(oid, name)
        self.assertEqual(name, t.name)
        self.assertEqual(oid, t.oid)

    def test_adding_adds_to_members(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f")
        tm2 = TeamMember(6, "g", "g")
        tm3 = TeamMember(7, "h", "h")
        t.add_member(tm1)
        self.assertIn(tm1, t.members)
        self.assertNotIn(tm2, t.members)
        t.add_member(tm2)
        self.assertIn(tm1, t.members)
        self.assertIn(tm2, t.members)
        t.add_member(tm3)

    def test_removing_removes_from_members(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f")
        tm2 = TeamMember(6, "g", "g")
        t.add_member(tm1)
        t.add_member(tm2)
        t.remove_member(tm1)
        self.assertNotIn(tm1, t.members)
        self.assertIn(tm2, t.members)

    # def test_member_named(self):
    #     t = Team(1, "Flintstones")
    #     t.add_member(TeamMember(2, "Fred", "fred@bedrock"))
    #     t.add_member(TeamMember(3, "Barney", "barney@bedrock"))
    #     t.add_member(TeamMember(4, "Wilma", "wima@bedrock"))
    #     self.assertEqual(t.members[0], t.member_named("Fred"))
    #     self.assertEqual(t.members[2], t.member_named("Wilma"))
    #     self.assertEqual(t.members[1], t.member_named("Barney"))
    #     self.assertIsNone(t.member_named("fred"))

    def test_sends_email(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f@foo.com")
        tm2 = TeamMember(6, "g", "g@bar.com")
        t.add_member(tm1)
        t.add_member(tm2)
        fe = FakeEmailer()
        t.send_email(fe, "S", "M")
        self.assertIn("f@foo.com", fe.recipients)
        self.assertIn("g@bar.com", fe.recipients)
        self.assertEqual(2, len(fe.recipients))
        self.assertEqual("S", fe.subject)
        self.assertEqual("M", fe.message)

    def test_duplicate_oid(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "ff")
        tm2 = TeamMember(6, "g", "gg")
        tm3 = TeamMember(5, "h", "hh")
        t.add_member(tm1)
        self.assertIn(tm1, t.members)
        self.assertNotIn(tm2, t.members)
        t.add_member(tm2)
        self.assertIn(tm1, t.members)
        self.assertIn(tm2, t.members)
        with self.assertRaises(Exception):
            t.add_member(tm3)

    def test_duplicate_email_value_error(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "ff")
        tm2 = TeamMember(6, "g", "gg")
        tm3 = TeamMember(7, "h", "ff")
        tm4 = TeamMember(8, "i", "FF")
        t.add_member(tm1)
        self.assertIn(tm1, t.members)
        self.assertNotIn(tm2, t.members)
        t.add_member(tm2)
        self.assertIn(tm1, t.members)
        self.assertIn(tm2, t.members)
        with self.assertRaises(Exception):
            t.add_member(tm3)
        # Checks for case insensitivity
        with self.assertRaises(Exception):
            t.add_member(tm4)



