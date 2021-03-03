from models import db, connect_db, Jobseeker, Recruiter, Event
from forms import AddJobseekerForm, AddRecruiterForm, LoginForm, JobseekerEditForm, RecruiterEditForm, AddEventForm
import os
import requests
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from secrets import api_id, api_key, secret_key


CURR_USER_KEY = "curr_user"

API_BASE_URL = 'https://api.adzuna.com/v1/api/jobs/us/search/1'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///capstone-hr'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secret_key)

# toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def starter_page():
    """Show homepage before user signs up."""

    return render_template('index.html')

##############################################################################
# JOBSEEKER signup/login


@app.before_request
def add_user_to_g():
    '''If user is logged in, add curr user to Flask global.'''

    if CURR_USER_KEY in session:
        g.jobseeker = Jobseeker.query.get(session[CURR_USER_KEY])

    else:
        g.jobseeker = None


def do_login(jobseeker):
    '''Log in user.'''

    session[CURR_USER_KEY] = jobseeker.id


def do_logout():
    '''Logout user.'''

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/logout')
def logout():
    '''Handle logout.'''

    do_logout()
    flash("You have logged out!", 'success')
    return redirect("/")


@app.route('/jobseekers/signup', methods=["GET", "POST"])
def signup():
    '''Handle signup.'''

    form = AddJobseekerForm()

    if form.validate_on_submit():
        try:
            jobseeker = Jobseeker.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                profile_img=form.profile_img.data or Jobseeker.profile_img.default.arg,
                bio=form.bio.data,
                location=form.location.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken, please try again", 'danger')
            return render_template('jobseekers/signup.html', form=form)

        do_login(jobseeker)

        return redirect("/jobseekers/home")

    else:
        return render_template('jobseekers/signup.html', form=form)


@app.route('/jobseekers/login', methods=["GET", "POST"])
def login():
    '''Handle login.'''

    form = LoginForm()

    if form.validate_on_submit():
        jobseeker = Jobseeker.authenticate(form.username.data,
                                           form.password.data)

        if jobseeker:
            do_login(jobseeker)
            flash(f"Hello, {jobseeker.username}!", "success")
            session['username'] = jobseeker.username
            return redirect("/jobseekers/home")

        flash("Invalid username/password, please try again", 'danger')

    return render_template('jobseekers/login.html', form=form)


##############################################################################
# JOBSEEKER routes

@app.route('/jobseekers/home', methods=['GET', 'POST'])
def homepage():
    '''Show current user homepage.'''

    if g.jobseeker:
        jobseeker = Jobseeker.query.get(session[CURR_USER_KEY])

        responses = requests.get(
            API_BASE_URL,
            params={"app_id": api_id, "app_key": api_key,
                    "what": "esport", 'location0': 'US'}
        )
        res = responses.json()
        data = res['results']

        choices = []

        for d in data:
            choices.append(d['location']['display_name'])

        return render_template('jobseekers/home.html', jobseeker=jobseeker, data=data, choices=choices)
    else:
        return render_template('index.html')


@app.route('/jobseekers/<int:jobseeker_id>', methods=["GET", "POST"])
def profile(jobseeker_id):
    '''Update profile for current user.'''

    jobseeker = Jobseeker.query.get_or_404(jobseeker_id)

    if not g.jobseeker:
        flash("Access unauthorized, please login as Jobseeker to view this page", "danger")
        return redirect("/")

    jobseeker = g.jobseeker

    form = JobseekerEditForm(obj=jobseeker)

    if form.validate_on_submit():
        if Jobseeker.authenticate(jobseeker.username, form.password.data):
            jobseeker.first_name = form.first_name.data
            jobseeker.last_name = form.last_name.data
            jobseeker.username = form.username.data
            jobseeker.email = form.email.data
            jobseeker.profile_img = form.profile_img.data
            jobseeker.bio = form.bio.data,
            jobseeker.location = form.location.data

            db.session.commit()
            return redirect('/jobseekers/home')

        flash("Wrong password, please try again", 'danger')

    return render_template('jobseekers/edit.html', form=form)


@app.route('/jobseekers/favorites')
def search_location():
    '''Show favorite jobs page.'''

    return render_template('/jobseekers/favorites.html')

##############################################################################
# RECRUITER signup/login


@app.before_request
def add_recruiter_to_g():
    '''If user is logged in, add curr user to Flask global.'''

    if CURR_USER_KEY in session:
        g.recruiter = Recruiter.query.get(session[CURR_USER_KEY])

    else:
        g.recruiter = None


def do_login_recruiter(recruiter):
    '''Log in user.'''

    session[CURR_USER_KEY] = recruiter.id

##############################################################################
# RECRUITER routes


@app.route('/recruiters/signup', methods=["GET", "POST"])
def signup_recruiter():
    '''Handle signup.'''

    form = AddRecruiterForm()

    if form.validate_on_submit():
        try:
            recruiter = Recruiter.signup(
                username=form.username.data,
                company_name=form.company_name.data,
                email=form.email.data,
                password=form.password.data,
                profile_img=form.profile_img.data or Recruiter.profile_img.default.arg,
                about=form.about.data,
                location=form.location.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken, please try again", 'danger')
            return render_template('recruiters/signup.html', form=form)

        do_login_recruiter(recruiter)

        return redirect("/recruiters/home")

    else:
        return render_template('recruiters/signup.html', form=form)


@app.route('/recruiters/login', methods=["GET", "POST"])
def login_recruiters():
    '''Handle login.'''

    form = LoginForm()

    if form.validate_on_submit():
        recruiter = Recruiter.authenticate(form.username.data,
                                           form.password.data)

        if recruiter:
            do_login_recruiter(recruiter)
            flash(f"Hello, {recruiter.username}!", "success")
            session['username'] = recruiter.username
            return redirect("/recruiters/home")

        flash("Invalid username/password, please try again", 'danger')

    return render_template('recruiters/login.html', form=form)


@app.route('/recruiters/home')
def homepage_recruiters():
    '''Show homepage after recruiter logs in.'''

    if g.recruiter:
        recruiter = Recruiter.query.get(session[CURR_USER_KEY])

        events = Event.query.all()

        return render_template('recruiters/home.html', recruiter=recruiter, events=events)

    else:
        flash("Access unauthorized, please login as Recruiter to view the page", "danger")
        return redirect("/")
        return render_template('index.html')


@app.route('/recruiters/<int:recruiter_id>', methods=["GET", "POST"])
def profile_recruiters(recruiter_id):
    '''Update profile for current user.'''

    recruiter = Recruiter.query.get_or_404(recruiter_id)

    if not g.recruiter:
        flash("Access unauthorized, please try again", "danger")
        return redirect("/")

    recruiter = g.recruiter

    form = RecruiterEditForm(obj=recruiter)

    if form.validate_on_submit():
        if Recruiter.authenticate(recruiter.username, form.password.data):
            recruiter.username = form.username.data
            recruiter.company_name = form.company_name.data
            recruiter.email = form.email.data
            recruiter.profile_img = form.profile_img.data
            recruiter.about = form.about.data,
            recruiter.location = form.location.data

            db.session.commit()
            return redirect('/recruiters/home')

        flash("Wrong password, please try again", 'danger')

    return render_template('recruiters/edit.html', form=form)


@app.route('/events')
def events_list():
    '''Show events list.'''

    events = Event.query.all()
    recruiters = Recruiter.query.all()
    jobseekers = Jobseeker.query.all()

    return render_template('events.html', events=events, recruiters=recruiters, jobseekers=jobseekers)


@app.route('/events/new', methods=['GET', 'POST'])
def create_event():
    '''Create a new event and add to the event list'''

    if not g.recruiter:
        flash("Access unauthorized, please login as Recruiter to view this page", "danger")
        return redirect("/")

    recruiter = g.recruiter

    form = AddEventForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        date = form.date.data
        location = form.location.data

        new_event = Event(title=title, description=description,
                          date=date, location=location, recruiters_id=recruiter.id)
        g.recruiter.events.append(new_event)
        db.session.commit()
        return redirect('/recruiters/home')
    else:
        return render_template('new_event.html', form=form)


@app.route('/events/<int:event_id>/delete', methods=['GET', 'POST'])
def delete_event(event_id):
    '''Delete an event.'''

    if not g.recruiter:
        flash("Access unauthorized, please login as Recruiter to view this page", "danger")
        return redirect("/")

    event = Event.query.get(event_id)

    db.session.delete(event)
    db.session.commit()

    return redirect('/recruiters/home')
