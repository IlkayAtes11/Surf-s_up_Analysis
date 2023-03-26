import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup

from flask import Flask

# Create an app, being sure to pass __name__
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Precipitation Analysis
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query the last 12 months of precipitation data
    last_12_months_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    
    last_12_months_prcp_dict = dict(last_12_months_prcp)
    
    return jsonify(last_12_months_prcp_dict)

# List of Stations
@app.route("//api/v1.0/stations")
def stations():

# Query the names of the all stations
    stations = session.query(Station.name).all()

    session.close()
    stations_dict = dict(stations)
    return jsonify(stations_dict)

# Most Active Station
@app.route("/api/v1.0/tobs")
def tobs():

# Query the most active stations`s date and temperature observations
    active_station= session.query(Measurement.station, Measurement.date, Measurement.tobs).filter_by(station = 'USC00519281').filter(Measurement.date >= '2016-08-23').all()

    active_station_dict = dict(active_station)
    return jsonify(active_station)


@app.route("/api/v1.0/start")
def start(start):

    min_avg_max = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    tobs = []

    for min,avg,max in min_avg_max:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs.append(tobs_dict)
        
    return jsonify(tobs)

@app.route("/api/v1.0/start_end")
def start_end(start,end):
    minavgmax_start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                func.max(Measurement.tobs)).filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()

    tobs = []
    for min,avg,max in minavgmax_start_end:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs.append(tobs_dict)

    return jsonify(tobs)


    session.close


if __name__ == "__main__":
    app.run(debug=True)
