from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)


class Jobseeker(db.Model):
    '''Jobseekers in the system.'''

    __tablename__ = 'jobseekers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    profile_img = db.Column(
        db.Text, default="/static/jobseeker.png")
    bio = db.Column(db.Text)
    location = db.Column(db.Text)

    @classmethod
    def signup(cls, first_name, last_name, username, email, password, profile_img, bio, location):
        """Sign up Jobseeker. Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        jobseeker = Jobseeker(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=hashed_pwd,
            profile_img=profile_img,
            bio=bio,
            location=location
        )

        db.session.add(jobseeker)
        return jobseeker

    @classmethod
    def authenticate(cls, username, password):
        """Find jobseeker with 'username' and 'password'."""

        jobseeker = cls.query.filter_by(username=username).first()

        if jobseeker:
            is_auth = bcrypt.check_password_hash(jobseeker.password, password)
            if is_auth:
                return jobseeker

        return False


class Recruiter(db.Model):
    '''Jobseekers in the system.'''

    __tablename__ = 'recruiters'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    company_name = db.Column(db.Text, nullable=False, unique=True)
    profile_img = db.Column(
        db.Text, default="/static/company.png")
    about = db.Column(db.Text)
    password = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text)

    events = db.relationship('Event')

    @classmethod
    def signup(cls, username, email, company_name, password, profile_img, about, location):
        """Sign up Recruiter. Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        recruiter = Recruiter(
            username=username,
            email=email,
            company_name=company_name,
            password=hashed_pwd,
            profile_img=profile_img,
            about=about,
            location=location
        )

        db.session.add(recruiter)
        return recruiter

    @classmethod
    def authenticate(cls, username, password):
        """Find recruiter with 'username' and 'password'."""

        recruiter = cls.query.filter_by(username=username).first()

        if recruiter:
            is_auth = bcrypt.check_password_hash(recruiter.password, password)
            if is_auth:
                return recruiter

        return False


class Event(db.Model):
    '''Events in the system.'''

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False, unique=True)
    date = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    recruiters_id = db.Column(db.Integer, db.ForeignKey(
        'recruiters.id', ondelete='CASCADE'), nullable=False)

    recruiter = db.relationship('Recruiter')
