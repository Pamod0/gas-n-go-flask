# This file includes all routes related to authentication process
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User  # import user from auth.py file
from .models import Station
from .models import Admin
from werkzeug.security import generate_password_hash, check_password_hash  # for hash passwords
from . import db                                                           # (secure passwords using encryption)
from flask_login import login_user, login_required, logout_user, current_user  # flask login module to help login tasks
                                                         # current user has attributes about logged/logged out in users 

auth = Blueprint('auth', __name__)  # blueprints have routes defined inside.
                                    # we can have our routes in seperate files, well organized.

# route for user login
@auth.route('/login', methods=['GET', 'POST'])  # GET and SET http requests
def login():  
    if request.method == 'POST':
        email = request.form.get('email')  # gather information
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()  # check user by email
        if user:
            if check_password_hash(user.password, password):  # if user's hash password matched
                flash('Logged in successfully!', category='success')  # flash messages
                login_user(user, remember=True)  # login user and  keep remebered that user is logged in
                return redirect('user_home')  # redirect to this page
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login_usr.html", user=current_user)  # this html page assigned to this function


# route for fuel station login
@auth.route('/login_station', methods=['GET', 'POST'])  # station login
def login_station():  
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        station = Station.query.filter_by(email=email).first()
        if station:
            if check_password_hash(station.password, password):
                flash('Logged in successfully!', category='success')
                login_user(station, remember=True)
                return redirect(url_for('views.station'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login_station.html", user=current_user)


# route for admin login
@auth.route('/login_admin', methods=['GET', 'POST'])  # admin login
def login_admin():  
    if request.method == 'POST':
        email = request.form.get('email')  
        password = request.form.get('password')

        admin = Admin.query.filter_by(email=email).first()  
        if admin:
            if check_password_hash(admin.password, password): 
                flash('Logged in successfully!', category='success') 
                login_user(admin, remember=True)  
                return redirect(url_for('views.adminDash'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login_admin.html", user=current_user)


# customer signup
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        vehicle_num = request.form.get('vehicleNum')
        vehicle_type = request.form.get('vehicleType')
        fuel_type = request.form.get('fuelType')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')  # meessage flash
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, vehicle_num = vehicle_num, 
                vehicle_type = vehicle_type, fuel_type = fuel_type, 
                password=generate_password_hash(password1, method='sha256'))  # create a new user
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.user'))

    return render_template("sign_up.html", user=current_user)


# fuel station signup
@auth.route('/sign-up_station', methods=['GET', 'POST'])  # station signup
def sign_up_station():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('stationName')
        phone = request.form.get('phone')
        password3 = request.form.get('password3')
        password4 = request.form.get('password4')

        station = Station.query.filter_by(email=email).first()
        if station:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(phone) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password3 != password4:
            flash('Passwords don\'t match.', category='error')
        elif len(password3) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Station(email=email, name=name, phone=phone, password=generate_password_hash(
                password3, method='sha256'))  # hashing password with specific hasing algorithm
            db.session.add(new_user)  # add new station to database
            db.session.commit()  # update the database with changes
            login_user(new_user, remember=True)  # login station and  keep remebered that station is logged in
            flash('Account created!', category='success')
            return redirect(url_for('views.station'))  # redirect to page

    return render_template("signup_station.html", user=current_user)


# admin signup
@auth.route('/sign-up_admin', methods = ['GET', 'POST'])  # admin signup
def sign_up_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password3 = request.form.get('password3')
        password4 = request.form.get('password4')

        admin = Admin.query.filter_by(email=email).first()
        if admin:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password3 != password4:
            flash('Passwords don\'t match.', category='error')
        elif len(password3) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Admin(email=email, name=name, password=generate_password_hash(
                password3, method='sha256')) 
            db.session.add(new_user) 
            db.session.commit()  
            login_user(new_user, remember=True) 
            flash('Account created!', category='success')
            return redirect(url_for('views.adminDash'))

    return render_template("sign_up_admin.html", user=current_user)


# logout route
@auth.route('/logout')  # logout
def logout():
    logout_user()
    flash('Log out successfully', category='success')
    return redirect(url_for('views.start'))

    
