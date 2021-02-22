from models import Event, db
from app import app

db.drop_all()
db.create_all()

event1 = Event(title='Hiring event!', description='Hiring for multiple roles like Lorem Ipsum dolor',
               date='August 5th', location='New York')
db.session.add(event1)
db.session.commit()
