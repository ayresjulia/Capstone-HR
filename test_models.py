from app import app
import os
from flask import session
from unittest import TestCase
from models import db, connect_db, Jobseeker, Recruiter, Event

os.environ["DATABASE_URL"] = "postgresql:///capstone-hr"

db.create_all()


class UserTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        j1 = Jobseeker.signup(first_name="testuser",
                                         last_name="testuser",
                                         username="testuser",
                                         email="test@me.com",
                                         password="testuser",
                                         profile_img=None,
                                         bio="bio",
                                         location="location")
        jid1 = 1111
        j1.id = jid1

        r1 = Recruiter.signup(username="testR",
                              email="testR",
                              company_name="testR",
                              password="testR",
                              profile_img=None,
                              about="testR",
                              location="testR")
        rid1 = 2222
        r1.id = rid1

        db.session.commit()

        j1 = Jobseeker.query.get(jid1)
        r1 = Recruiter.query.get(rid1)

        self.j1 = j1
        self.jid1 = jid1

        self.r1 = r1
        self.rid1 = rid1

        self.client = app.test_client()

    def test_authenticate(self):
        """Testing authentication of a user."""

        j1 = Jobseeker.authenticate(self.j1.username, "password")
        self.assertIsNotNone(j1)

        self.assertFalse(Jobseeker.authenticate("badusername", "password"))

        self.assertFalse(Jobseeker.authenticate(
            self.j1.username, "badpassword"))

        r1 = Recruiter.authenticate(self.r1.username, "password")
        self.assertIsNotNone(r1)

        self.assertFalse(Recruiter.authenticate("badusername", "password"))

        self.assertFalse(Recruiter.authenticate(
            self.r1.username, "badpassword"))
