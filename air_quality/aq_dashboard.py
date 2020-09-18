from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy
from openaq import OpenAQ
import openaq

api = openaq.OpenAQ()

"""OpenAQ Air Quality Dashboard with Flask."""
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)

@APP.route('/')
def root():
  
  return 'TODO - part 2 and beyond!'

def citysplit(city='Los Angeles', parameter='pm25'):
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    la_results = body['results']
    date = []
    for a in la_results:
        for x, y in a.items():
            if x == 'date':
                date.append(y)

    utc = []
    for p in date:
        for k, l in p.items():
            if k == 'utc':
                utc.append(l)

    val = []
    for d in la_results:
        for m, n in d.items():
            if m == 'value':
                val.append(n)

    utc_value = list(zip(utc,val))
    return utc_value

##########################################################

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)
    def __repr__(self):
        return 'TODO - write a nice representation of Records'


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    utc_value = citysplit(city='Los Angeles', parameter='pm25')
    for x in utc_value:
        db_record = Record(datetime=x[0], value=x[1])
        DB.session.add(db_record)


    DB.session.commit()
    return 'Data refreshed!'
