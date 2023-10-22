'''
Hackathon 2023 Team 8
Team Members: Callie Campbell-Perdomo, Sam Candaleria, Saul Gonzalez, Saul's friend, Vincent Dufour
Description: Student-made website for students containing student-crowdsourced info & reviews
'''

from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, PasswordField, BooleanField, SubmitField, Form, FieldList, FormField, SelectField, DateField, validators)
from wtforms.validators import DataRequired, Optional, NumberRange


class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    student_id = StringField('Student ID', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    passwd_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class SignInForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class EventCreationForm(FlaskForm):
    date = DateField('Event Date', validators=[DataRequired()])
    desc = StringField("Description of Event",validators=[DataRequired()])
    rsvp = StringField('RSVP',validators=[Optional()])
    submit = SubmitField('Confirm')

class EventRSVPForm(FlaskForm):
    date = DateField('Event Date', validators=[DataRequired()])
    desc = StringField("Description of Event",validators=[DataRequired()])
    rsvp = StringField('RSVP',validators=[Optional()])
    submit = SubmitField('Confirm')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (out of 5):',validators=[DataRequired(), NumberRange(min=0, max=5, message="Please rate out of 5.")])
    comments = StringField('Comment:',validators=[Optional()])
    submit = SubmitField('Confirm')

class FoodCreate(FlaskForm):
    id = IntegerField('Unique ID',validators=[DataRequired()])
    name = StringField('Restaurant Name',validators=[DataRequired()])
    location = StringField('Location',validators=[DataRequired()])
    image = StringField('Image',validators=[Optional()])
    submit = SubmitField('Create New Restaurant')

class FoodEdit(FlaskForm):
    id = IntegerField('Unique ID',validators=[DataRequired()])
    name = StringField('Restaurant Name',validators=[DataRequired()])
    location = StringField('Location',validators=[DataRequired()])
    image = StringField('Image',validators=[Optional()])
    submit = SubmitField('Confirm Changes')