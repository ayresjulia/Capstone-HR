# Talisman Gaming Job Search App

![homepage_gif](./static/homepage.gif)
![jobseeeker_gif](./static/jobseeker.gif)
![recruiter_gif](./static/recruiter.gif)

## Description

Talisman was created to connect Recruiters and Jobseekers in the Gaming industry with ease of use. Talisman strives to create a welcoming environment with an easy way for users to browse through it. Jobseekers can apply for jobs, save them to favorites, browse open events and save them as well to RSVP later. Recruiters are able to create new events, and view all future events available. The idea is to connect recruiters to jobseekers by attending posted events and networking.

## Features

- access the website as a Jobseeker or a Recruiter, and discover different features
  for jobseekers:
- view upcoming events without signing up
- view available jobs on the home page
- save jobs to favorites to apply later
- apply from home page and get redirected to Adzuna website for more information about the job
- save events to favorites
  for recruiters:
- post new events
- delete posted events

## Installation

- clone repository using command line
  
```
$ git clone https://github.com/ayresjulia/Capstone-HR.git
```

- create virtual environment and activate it

```
$ python3 -m venv venv
$ source venv/bin/activate
```

- install all requirements 

```
$ pip install -r requirements.txt
```

- start the app in localhost

```
$ flask run
```

## Tests

- to run tests, use respective commands in command line
  
```
$ python3 -m test_app.py
$ python3 -m test_models.py
```

## API Used

[Adzuna API](https://api.adzuna.com)

## Tech Stack

- Web/Frontend
  - JavaScript | CSS | HTML
  
- Frontend Libraries/Frameworks
  - Bootstrap | jQuery | Axios | Jinja
  
- Server/Backend
  - Python | SQL | PostgreSQL

- Backend Libraries/Frameworks
  - Flask | Flask-SQLAlchemy

## Database Schema

![db_image](./static/db.png)

## User Flow

![userflow_image](./static/userflow0.png)

## Talisman Gaming Job Search App v2.0

- connect jobseekers and events db tables, by creating favorite events feature