'''
Hackathon 2023 Team 8
Team Members: Callie Campbell-Perdomo, Sam Candaleria, Saul Gonzalez, Saul's friend, Vincent Dufour
Description: Student-made website for students containing student-crowdsourced info & reviews
'''

from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, PasswordField, BooleanField, SubmitField, Form, FieldList, FormField, SelectField, validators)
from wtforms.validators import DataRequired, Optional


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
    date = StringField("Date",validators=[DataRequired()])
    desc = StringField("Description of Event",validators=[DataRequired()])
    submit = SubmitField('Confirm')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating',validators=[DataRequired()])
    comments = StringField('Leave a Comment!',validators=[Optional()])
    submit = SubmitField('Confirm')