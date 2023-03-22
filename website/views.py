# Other routes are included in this page
from os import abort
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .models import User
from .models import FuelInfo
from .models import Quota
from . import db

views = Blueprint('views', __name__)  # blueprints have routes defined inside.
                                      # we can have our routes in seperate files, well organized.

@views.route('/')  # create a route in webpage. this is home page
def start():
    return render_template("start.html")  # render specific html file


#user routes
@views.route('/user_home')  # user homepage
@login_required  # login required to view this page
def user():
    return render_template("user_home.html")


@views.route('/my_data')  # print user database table to website
def daTa():
    return render_template("my_data.html", datA = User.query.all())


@views.route('/my_quota')  # print user's quota database table to website
def quota():
    return render_template("my_quota.html", datA = Quota.query.all())


@views.route('/find_fuel') # show currently available fuel stations
def findFuel():
    fuel = FuelInfo.query.all()
    return render_template("userFuel.html", fuel = fuel)


@views.route('/admin_dash')  # admin dashboard
@login_required 
def adminDash():
    return render_template("admin_dashboard.html")


# station routes
@views.route('/station_home')  # station homepage
def station():
    return render_template("station_home.html") 


# routes for fuel station status update
@views.route('/stationUpdate' , methods = ['GET','POST'])
def stUpdate():
    if request.method == 'GET':
        return render_template('stationUpdate.html')
 
    if request.method == 'POST':

        statUs = request.form.getlist('status')
        status=",".join(map(str, statUs))


        station_name = request.form['station_name']
        phone = request.form['phone']
        fuel_availability = request.form['fuel_availability']
        status = status
        fuel = FuelInfo(
            station_name=station_name,
            phone=phone,
            fuel_availability=fuel_availability, 
            status=status
        )
        db.session.add(fuel)
        db.session.commit()
        return redirect('/stationUpdate')


@views.route('/stinfo')  # display added station data 
def retrieveList():
    fuel = FuelInfo.query.all()
    return render_template('stationInfo.html',fuel = fuel)


@views.route('/<int:id>/edit',methods = ['GET','POST'])  # edit info
def update(id):                                     # must pass integer(id)
    fuEl = FuelInfo.query.filter_by(id=id).first()  # fuel station info databse
    if request.method == 'POST':
        if fuEl:
            db.session.delete(fuEl)
            db.session.commit()

        statUs = request.form.getlist('status')
        status =  ",".join(map(str, statUs)) 
        station_name = request.form['station_name']
        phone = request.form['phone']
        fuel_availability = request.form['fuel_availability']
        status = status 

        fuEl = FuelInfo(
            station_name=station_name,
            phone=phone,
            fuel_availability=fuel_availability, 
            status=status
        )
        db.session.add(fuEl)
        db.session.commit()
        return redirect('/stinfo')
        return f"Station with id = {id} Does nit exist"
 
    return render_template('updateData.html', fuEl = fuEl)


@views.route('/<int:id>/delete', methods=['GET','POST'])  # delete info
def delete(id):
    fuel = FuelInfo.query.filter_by(id=id).first()
    if request.method == 'POST':
        if fuel:
            db.session.delete(fuel)
            db.session.commit()
            return redirect('/stinfo')
        abort(404)
    return render_template('delete.html')


# routes for fuel quota update
@views.route('/qUpdate' , methods = ['GET','POST'])
def qUpdate():
    if request.method == 'GET':
        return render_template('qUpdate.html')
 
    if request.method == 'POST':

        user_id = request.form['user_id']
        quota = request.form['quota']
        qta = Quota(
            user_id=user_id,
            quota=quota
        )
        db.session.add(qta)
        db.session.commit()
        return redirect('/qUpdate')


@views.route('/qInfo')  # display added quota data 
def retrieveQ():
    qta = Quota.query.all()
    return render_template('qInfo.html',qta = qta)


@views.route('/<int:id>/qedit',methods = ['GET','POST'])  # edit info
def qedit(id):                                     # must pass integer(id)
    qT = Quota.query.filter_by(id=id).first()  # fuel quota databse
    if request.method == 'POST':
        if qT:
            db.session.delete(qT)
            db.session.commit()

        user_id = request.form['user_id']
        quota = request.form['quota']

        qT = Quota(
            user_id=user_id,
            quota=quota
        )
        db.session.add(qT)
        db.session.commit()
        return redirect('/qInfo')
        return f"Quota with id = {id} Does nit exist"
 
    return render_template('qupdateData.html', qT=qT)


@views.route('/<int:id>/qdelete', methods=['GET','POST'])  # delete info
def qdelete(id):
    qta = Quota.query.filter_by(id=id).first()
    if request.method == 'POST':
        if qta:
            db.session.delete(qta)
            db.session.commit()
            return redirect('/qInfo')
        abort(404)
    return render_template('delete.html')