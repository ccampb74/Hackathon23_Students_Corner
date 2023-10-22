'''
Hackathon 2023 Team 8
Team Members: Callie Campbell-Perdomo, Sam Candaleria, Saul Gonzalez, Saul's friend, Vincent Dufour
Description: Student-made website for students containing student-crowdsourced info & reviews
'''

from app import app, db, load_user
from app.models import User, Event, Review, Food
from app.forms import SignUpForm, SignInForm, EventCreationForm, ReviewForm
from flask import render_template, redirect, url_for, request, redirect
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html',user=current_user)


###########################################################################################################
# Start of sign in/ sign-up/ sign out 


# sign-in functionality
@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    form = SignInForm()
    if form.validate_on_submit():
        id = form.id.data
        passwd = form.passwd.data
        hashed_passwd = passwd.encode('utf-8')

        user = load_user(id)

        if user:
            if bcrypt.checkpw(hashed_passwd, user.passwd):
                login_user(user)
            else:
                return '<p>Incorrect Password!</p>'

            if user.id == "admin":
                return redirect(url_for('index_admin'))
            else:
                return redirect(url_for('index'))
        else:
            return '<p>Username not recognized!</p>'
    else:
        return render_template('users_signin.html', title=app.config['USER SIGNIN'], form=form)


# sign-up functionality
@app.route('/users/signup', methods=['GET', 'POST'])
def users_signup():
    form = SignUpForm()
    if form.validate_on_submit():
        passwd = form.passwd.data
        passwd_confirm = form.passwd_confirm.data
        if passwd == passwd_confirm:
            hashed = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
        else:
            return '<p>Passwords do not match!</p>'
        
        new_user = User(
            id = form.id.data,
            student_id = form.student_id.data,
            email = form.email.data,
            passwd = hashed
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        return render_template('users_signup.html', title=app.config['USER SIGNUP'], form=form)


# sign-out functionality
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    logout_user()
    return redirect(url_for('index'))


# new event
@app.route('/users/newevent', methods=['GET', 'POST'])
@login_required
def create_event():
    form= EventCreationForm()
    if form.validate_on_submit():
        new_event = Event(
            date = form.date.data,
            desc = form.desc.data,
            rsvp = 1,
            user_id = current_user.id,
            food_id = '1234'
        )
        
        return render_template('create_event.html', title=app.config['CREATE EVENT'], form=form)


# End of sign in/ sign-up/ sign out 
###########################################################################################################


###########################################################################################################
# Start of user-facing routes

@app.route('/restaurant')
def testing_restaurants():
    return render_template('food_place.html')


# End of user-facing routes 
###########################################################################################################


###########################################################################################################
# Start of admin-facing routes


@app.route('/indexadmin')
def index_admin():
    return render_template('index_admin.html', user=current_user)

@app.route('/users')
#@login_required     
def list_users(): 
    users = User.query.all()
    return render_template('users.html', users=users)
    

# End of admin-facing routes 
###########################################################################################################
