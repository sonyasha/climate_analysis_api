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
            f'Check last year temperature: /api/v1.0/precipitation<br/>'
    )


@app.route('/api/v1.0/precipitation')
def last_year_temp():
    '''Dates and temperature observations from the last year'''
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    year_ago = date - dt.timedelta(days=365)
    res = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > year_ago).all()
    tdict = {}
    for r in res:
        tdict[r[0]] = r[1]
    return jsonify(tdict)


if __name__ == '__main__':
    app.run(debug=True)
