'''
Hackathon 2023 Team 8
Team Members: Callie Campbell-Perdomo, Sam Candaleria, Saul Gonzalez, Saul's friend, Vincent Dufour
Description: Student-made website for students containing student-crowdsourced info & reviews
'''

from app import db
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from datetime import date


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    student_id = db.Column(db.String)
    email = db.Column(db.String)
    passwd = db.Column(db.LargeBinary)
    reviews= db.relationship("Review")
    events= db.relationship("Event")

class Event(db.Model):
    __tablename__= 'event'
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.String)
    desc = db.Column(db.String)
    rsvp = db.Column(db.Integer)
    food_id = mapped_column(ForeignKey("food.id"))
    food = relationship("Food", back_populates="events")
    user_id= db.column

class Food(db.Model):
    __tablename__= 'food'
    id = db.Column(db.String, primary_key=True)
    name = db.column(db.String)
    location = db.column(db.String)
    event_id = mapped_column(ForeignKey("event.id"))
    events = relationship("Event", back_populates="foods")

class Review(db.model):
    __tablename__= 'review'



