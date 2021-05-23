from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

app = Flask(__name__)
@app.route("/")
def routes():
    return(
        f"Welcome to my humble API!<br/>"
        f"Available routes include!<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")



engine = create_engine("sqlite:///Homework/sqlalchemy_challenge/Resources/hawaii.sqlite")
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



if __name__ == "__main__":
    app.run(debug=True)