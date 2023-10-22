'''
Hackathon 2023 Team 8
Team Members: Callie Campbell-Perdomo, Sam Candaleria, Saul Gonzalez, Saul's friend, Vincent Dufour
Description: Student-made website for students containing student-crowdsourced info & reviews
'''

from app import app, db, load_user
from app.models import User, Event, Review, Food
from app.forms import SignUpForm, SignInForm, EventCreationForm, ReviewForm, FoodCreate, FoodEdit
from flask import render_template, redirect, url_for, request, redirect
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt
from sqlalchemy import cast, Integer
from datetime import date


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    todays_date = date.today().strftime('%Y%m%d')
    print (todays_date)
    date_int = int(todays_date)
    print (date_int)
    five_events= db.session.query(Event).filter(cast((Event.date).replace("-",""), Integer) >= todays_date).limit(5).all()
    print (five_events)
    return render_template('index.html',user=current_user, five_events=five_events)


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
        return render_template('users_signin.html', title=app.config['USER SIGNIN'], form=form,user=current_user)


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
        return render_template('users_signup.html', title=app.config['USER SIGNUP'], form=form,user=current_user)


# sign-out functionality
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    logout_user()
    return redirect(url_for('index'))





# End of sign in/ sign-up/ sign out 
###########################################################################################################


###########################################################################################################
# Start of user-facing routes

@app.route('/restaurant')
def testing_restaurants():
    restaurants = Food.query.all()
    return render_template('food_place.html',user=current_user, restaurants=restaurants)

@app.route('/displayreview', methods=['GET'])
def display_review():
    show_review = Review.query.all()
    return render_template('display_review.html', show=show_review)


@app.route('/testreview', methods=['GET', 'POST'])
def review():
    form = ReviewForm()
    
    if form.validate_on_submit():
        print('in if')
        test_review = Review(
                    rating=form.rating.data,
                    comments=form.comments.data,
                    user=form.user_id.data
                )
        
        db.session.add(test_review)
        db.session.commit()

        return redirect(url_for('display_review'))
    else:
        print('in else')
        return render_template('testreview.html', title=app.config['TEST_REVIEW'], form=form, user=current_user) 
    
# new event
@app.route('/users/newevent', methods=['GET', 'POST'])
@login_required
def create_event():
    form= EventCreationForm()
    if form.validate_on_submit():
        if not db.session.query(Event).order_by(Event.id.desc()).first():
                newid = 1
        else:
                last_event = db.session.query(Event).order_by(Event.id.desc()).first()
                print ("aaaaa", last_event)
                newid = int(last_event.id) + 1
                print ("blah", newid)

        new_event = Event(
            id= newid,
            date = form.date.data,
            desc = form.desc.data,
            rsvp = 1,
            user_id = current_user.id,
            food_id = '1111'
        )

        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for('list_events'))
    else:   
        return render_template('create_event.html', form=form, user=current_user)
    



# End of user-facing routes 
###########################################################################################################


###########################################################################################################
# Start of admin-facing routes

# admin home page
@app.route('/indexadmin', methods=['GET', 'POST'])
def index_admin():
    foods = Food.query.all()
    return render_template('index_admin.html', user=current_user, foods=foods)


# restaurant creation page
@app.route('/indexadmin/restaurant/create', methods=['GET', 'POST'])
def restaurant_create():
    form = FoodCreate()
    if form.validate_on_submit():

        new_restaurant = Food(
            id=form.id.data,
            name=form.name.data,
            location=form.location.data,
            image=form.image.data
        )

        db.session.add(new_restaurant)
        db.session.commit()

        return redirect(url_for('index_admin'))
    else:
        return render_template('restaurant_create.html',form=form, user=current_user)
    
# restaurant edit
@app.route('/indexadmin/restaurant/<id>/edit', methods=['GET', 'POST'])
@login_required
def restaurant_edit(id):
    restaurant_to_edit = db.session.query(Food).get(id)
    form = FoodEdit(obj=restaurant_to_edit)

    if form.validate_on_submit():
        form.populate_obj(restaurant_to_edit)
        db.session.commit()

        return redirect(url_for('index_admin'))
    else:
        return render_template('restaurant_create.html', form=form, id=restaurant_to_edit, user=current_user)


# restaurant deletion
@app.route('/indexadmin/restaurant/<id>/delete', methods=['GET', 'POST'])
@login_required
def restaurant_delete(id):
    restaurant_to_delete = db.session.query(Food).filter(Food.id == id).one()

    db.session.delete(restaurant_to_delete)
    db.session.commit()

    return redirect(url_for('index_admin'))

# users listing page
@app.route('/users')
#@login_required     
def list_users(): 
    users = User.query.all()
    return render_template('users.html', users=users, user=current_user)

@app.route('/events')
#@login_required     
def list_events(): 
    events= Event.query.filter_by(food_id='1111').all()
    return render_template('events.html', events=events, user=current_user)
    

# End of admin-facing routes 
###########################################################################################################
