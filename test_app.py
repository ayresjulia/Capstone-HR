from app import app, CURR_USER_KEY
import os
from flask import session
from unittest import TestCase
from models import db, connect_db, Jobseeker, Recruiter, Event

os.environ["DATABASE_URL"] = "postgresql:///capstone-hr"

db.create_all()


class AppTestCase(TestCase):

    def test_starter_page(self):
        """Ensuring homepage works."""

        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("We provide Esport Jobs in one place", html)

    def test_logout(self):
        """Ensuring redirect works when loggin out."""

        with app.test_client() as client:
            res = client.get("/logout")
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/")

    def setUp(self):
        """Create test client, add sample data."""

        Jobseeker.query.delete()
        Recruiter.query.delete()

        self.client = app.test_client()

        self.testuser = Jobseeker.signup(first_name="test",
                                         last_name="test",
                                         username="test",
                                         email="test@meo.com",
                                         password="test",
                                         profile_img=None,
                                         bio="bio",
                                         location="location")
        self.testuser_id = 7236
        self.testuser.id = self.testuser_id

        self.testuser2 = Recruiter.signup(username="abc",
                                          email="abcR@test.com",
                                          company_name="abc",
                                          password="asdfghjkl",
                                          profile_img=None,
                                          about="abc",
                                          location="abc")
        self.testuser2_id = 6534
        self.testuser2.id = self.testuser2_id

        db.session.commit()

    def test_homepage(self):
        """Show Jobseeker home page after loging in."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            res = c.get("/jobseekers/home")
            html = res.get_data(as_text=True)
            self.assertIn("Hi", html)

    def test_js_redirect(self):
        """Make sure Jobseeker cannot access Recruiter Homepage."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            res = c.get("/recruiters/home")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 302)

    def test_search_location(self):
        """Make sure Jobseeker can access Favorites Page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            res = c.get("/jobseekers/favorites")
            html = res.get_data(as_text=True)
            self.assertIn("Got Favorites?", html)

    def test_create_event(self):
        """Make sure Jobseeker cannot create new event/access new event page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            res = c.get("/events/new")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 302)

    def test_homepage_recruiters(self):
        """Show Recruiter home page after loging in."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser2.id

            res = c.get("/recruiters/home")
            html = res.get_data(as_text=True)
            self.assertNotIn("Favorites", html)

    def test_rec_redirect(self):
        """Make sure Recruiter cannot access Jobseeker Homepage."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser2.id

            res = c.get("/jobseekers/home")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("We provide Esport Jobs in one place!", html)

    def test_favorites(self):
        """Make sure Recruiter cannot access Jobseeker Favorites page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser2.id

            res = c.get("/jobseekers/favorites")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 302)
