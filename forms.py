from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.fields.html5 import EmailField

##############################################################################
# JOBSEEKER forms


class AddJobseekerForm(FlaskForm):
    """Add a User."""

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("E-mail", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])
    profile_img = StringField("(Optional) Profile Picture")
    bio = StringField("Bio", validators=[DataRequired()])
    location = StringField("Location (city, country)",
                           validators=[DataRequired()])


class JobseekerEditForm(FlaskForm):
    """Edit a User."""

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("E-mail", validators=[DataRequired()])
    profile_img = StringField("Profile Picture")
    bio = StringField("Bio", validators=[DataRequired()])
    location = StringField("Location (city, country)",
                           validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])


##############################################################################
# RECRUITER forms

class AddRecruiterForm(FlaskForm):
    """Add a User."""

    username = StringField("Username", validators=[DataRequired()])
    company_name = StringField("Company Name", validators=[Optional()])
    email = EmailField("E-mail", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])
    profile_img = StringField("(Optional) Company Logo")
    about = StringField("About", validators=[DataRequired()])
    location = StringField("Location (city, country)",
                           validators=[DataRequired()])


class RecruiterEditForm(FlaskForm):
    """Edit a User."""

    username = StringField("Username", validators=[DataRequired()])
    company_name = StringField("Company Name", validators=[Optional()])
    email = EmailField("E-mail", validators=[DataRequired()])
    profile_img = StringField("Profile Picture")
    about = StringField("About", validators=[DataRequired()])
    location = StringField("Location (city, country)",
                           validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])

##############################################################################
# GENERAL forms


class AddEventForm(FlaskForm):
    """Add new event."""

    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[Optional()])
    date = StringField("Date (MM-DD-YY)", validators=[DataRequired()])
    location = StringField("Location (city, state)",
                           validators=[DataRequired()])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])
