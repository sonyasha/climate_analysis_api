import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import os
os.chdir('/Users/sonik/Desktop/BC/GitHub/07-Weather_API/climate_analysis_api/Notebooks')

engine = create_engine('sqlite:///../Base/hawaii.sqlite')

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route('/')
def main_page():
    '''Some warm greeting and links'''
    print('main page opened')
    return (f'Welcome to Weather API page<br/>'
            f'Last year percipitations: /api/v1.0/precipitation<br/>'
            f'Station names: /api/v1.0/stations<br/>'
            f'Laxt year temperatures: /api/v1.0/tobs<br/>'
            f'Min, Avg and Max temperatures for the period %Y-%m-%d/%Y-%m-%d<br/>'
            f'or only from %Y-%m-%d: /api/v1.0/'
    )


@app.route('/api/v1.0/precipitation')
def last_year_prcp():
    '''Dates and precipitation observations from the last year'''
    print('last year precipitations opened')
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    year_ago = date - dt.timedelta(days=365)
    res = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago).all()
    tdict = {}
    for r in res:
        tdict[r[0]] = r[1]
    return jsonify(tdict)

@app.route('/api/v1.0/stations')
def stations():
    '''A list of stations'''
    print('station list opened')
    res = stations = session.query(Measurement.station).group_by(Measurement.station).all()
    rl = [r[0] for r in res]
    return jsonify(rl)

@app.route('/api/v1.0/tobs')
def last_year_temp():
    '''Dates and temperature observations from the last year'''
    print('last year temperatures opened')
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    year_ago = date - dt.timedelta(days=365)
    res = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > year_ago).all()
    tdict = {}
    for r in res:
        tdict[r[0]] = r[1]
    return jsonify(tdict)

@app.route('/api/v1.0/<start>')
def start_date(start):
    '''Minimum, average and the max temperature for a given start range'''
    print('start date entered')
    d = {}
    res = session.query((func.min(Measurement.tobs)), (func.avg(Measurement.tobs)), (func.max(Measurement.tobs))).\
    filter(Measurement.date >= start).all()
    t = [x for x in res[0]]
    d['MIN temperature'] = t[0]
    d['AVERAGE temperature'] = t[1]
    d['MAX temperature'] = t[2]
    return jsonify(d)

@app.route('/api/v1.0/<start>/<end>')
def both_dates(start,end):
    '''Minimum, average and the max temperature for a given start - end range'''
    print('start/end dates entered')
    d = {}
    res = session.query((func.min(Measurement.tobs)), (func.avg(Measurement.tobs)), (func.max(Measurement.tobs))).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    t = [x for x in res[0]]
    d['MIN temperature'] = t[0]
    d['AVERAGE temperature'] = t[1]
    d['MAX temperature'] = t[2]
    return jsonify(d)

if __name__ == '__main__':
    app.run(debug=True)
