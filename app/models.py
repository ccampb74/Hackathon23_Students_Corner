'''
Hackathon 2023 Team 8
Team Members: Callie Campbell-Perdomo, Sam Candaleria, Saul Gonzalez, Saul's friend, Vincent Dufour
Description: Student-made website for students containing student-crowdsourced info & reviews
'''

from app import db
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from datetime import date


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    student_id = db.Column(db.String)
    email = db.Column(db.String)
    passwd = db.Column(db.LargeBinary)
    reviews= db.relationship("Review")
    events= db.relationship("Event")

class Food(db.Model):
    __tablename__= 'foods'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    image = db.Column(db.String)
    events = relationship("Event")
    reviews = relationship("Review")
    
class Event(db.Model):
    __tablename__= 'events'
    food_id = db.Column(db.String, db.ForeignKey("foods.id"))
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    desc = db.Column(db.String)
    rsvp = db.Column(db.Integer)
    user_id= db.Column(db.String, db.ForeignKey("users.id"))
    user=db.relationship("User", back_populates="events")
    food_= db.relationship("Food")

class Review(db.Model):
    __tablename__= 'reviews'
    food = db.Column(db.String, db.ForeignKey("foods.id"), primary_key=True)
    rating = db.Column(db.Integer)
    comments = db.Column(db.String)
    user_id= db.Column(db.String, db.ForeignKey("users.id"))
    user_=db.relationship("User")




