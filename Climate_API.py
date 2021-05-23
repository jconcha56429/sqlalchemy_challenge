from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from sqlalchemy.sql.elements import Grouping

app = Flask(__name__)
@app.route("/")
def routes():
    return(
        f"Welcome to my humble API!<br/>"
        f"Available routes include!<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2017<br/>"
        f"/api/v1.0/2017/2018")



engine = create_engine("sqlite:///Homework/sqlalchemy_challenge/Resources/hawaii.sqlite",connect_args={'check_same_thread': False})
Base = automap_base()
Base.prepare(engine, reflect = True)
session = Session(engine)

measurement = Base.classes.measurement
station = Base.classes.station

@app.route('/api/v1.0/precipitation')
def precipitation():
    date1 = dt.datetime(2016,8,22)
    results = dict(session.query(measurement.date,measurement.prcp).filter(measurement.date > date1).all())
    return jsonify(results)

@app.route('/api/v1.0/stations')
def stations():
    results2 = list(session.query(station.name).all())
    return jsonify(results2)


@app.route('/api/v1.0/tobs')
def tobs():
    max_query = session.query(func.max(measurement.date)).first()[0]
    last_day = dt.datetime.strptime(max_query,'%Y-%m-%d').date()
    first_day = last_day - dt.timedelta(days=365)
    results3 = list(session.query(measurement.station,measurement.date,measurement.tobs).filter(measurement.date >= first_day).filter(measurement.station == "USC00519281").all())

    last_day_prev = first_day
    first_day_prev = first_day - dt.timedelta(days=365)
    results4 = list(session.query(measurement.tobs).filter(measurement.date > first_day_prev).filter(measurement.date < last_day_prev).filter(measurement.station == "USC00519281").all())
    return jsonify(results4)

    
@app.route('/api/v1.0/2016')
def start():
    dt_2016 = dt.datetime(2016,1,1)
    results_max = session.query(func.max(measurement.tobs)).filter(measurement.date > dt_2016).all()
    results_min = session.query(func.min(measurement.tobs)).filter(measurement.date > dt_2016).all()
    results_avg = session.query(func.avg(measurement.tobs)).filter(measurement.date > dt_2016).all()
    # gay = list(session.query(func.max(measurement.tobs),func.min(measurement.tobs),func.avg(measurement.tobs).filter(measurement.date > dt_2017)).all()) 
    return (f'Max: {results_max[0]} Min: {results_min[0]} Avg: {results_avg[0]} Temperatures after 2016')

@app.route('/api/v1.0/2016/2017')
def start_end():
    dt_2016 = dt.datetime(2016,1,1)
    dt_2017 = dt.datetime(2017,1,1)
    results_max_2 = session.query(func.max(measurement.tobs)).filter(measurement.date >= dt_2016).filter(measurement.date < dt_2017).all()
    results_min_2 = session.query(func.min(measurement.tobs)).filter(measurement.date >= dt_2016).filter(measurement.date < dt_2017).all()
    results_avg_2 = session.query(func.avg(measurement.tobs)).filter(measurement.date >= dt_2016).filter(measurement.date < dt_2017).all()

    return (f'Max: {results_max_2[0]} Min: {results_min_2[0]} Avg: {results_avg_2[0]} Temperatures from 2016 - 2017')


session.close()
if __name__ == "__main__":
    app.run(debug=True)

