                                # This file has all databases of system defined 

from . import db  # import db object from package
from flask_login import UserMixin  # help us login users and do simillar tasks
from sqlalchemy.sql import func  # for date/time
from datetime import datetime

                                                            
# model is like a blueprint. every note must be like this
class User(db.Model, UserMixin):  # create user table and inherite from UserMixin
    id = db.Column(db.Integer, primary_key=True)  # define columns
    email = db.Column(db.String(150), unique=True)  # email must be unique
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    vehicle_num = db.Column(db.Integer, unique=True)
    vehicle_type = db.Column(db.String(15))
    fuel_type = db.Column(db.String(10))


class Quota(db.Model):
    __tablename__ = "quota"  # overiding table name
 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    quota = db.Column(db.String())
 
    def __init__(self, user_id, quota):
        self.user_id = user_id
        self.quota = quota

    def __repr__(self):
        return f"{self.user_id}:{self.quota}"
    #  represent a class’s objects as a string

class Station(db.Model, UserMixin):  # fuel station databse
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(150), unique=True)  
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    phone = db.Column(db.Integer,unique=True)


class FuelInfo(db.Model):  # fuel station status database
    __tablename__ = "fuel"
 
    id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String())
    phone = db.Column(db.String())
    fuel_availability = db.Column(db.String())
    status = db.Column(db.String())
 
    def __init__(self, station_name, phone, fuel_availability, status):
        self.station_name = station_name
        self.phone = phone
        self.fuel_availability = fuel_availability
        self.status = status

    def __repr__(self):
        return f"{self.station_name}:{self.phone}"


class Admin(db.Model, UserMixin):  # admin databse
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(150), unique=True) 
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))


