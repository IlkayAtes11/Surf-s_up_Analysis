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

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the last 12 months of precipitation data
    last_12_months_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()

    session.close()

   # Dict with date as the key and prcp as the value
    date_precipitation = {date: prcp for date, prcp in precipitation}

    return jsonify(date_precipitation)

# List of Stations
@app.route("//api/v1.0/stations")
def stations():

# Create our session (link) from Python to the DB
    session = Session(engine)

# Query the names of the all stations
    stations = session.query(Station.name).all()

    session.close()
    stations = list(np.ravel(stations))
    return jsonify(stations)

# Most Active Station
@app.route("/api/v1.0/tobs")
def tobs():

# Create our session (link) from Python to the DB
    session = Session(engine)

# Query the most active stations`s date and temperature observations
    active_station= session.query(Measurement.station, Measurement.date, Measurement.tobs).filter_by(station = 'USC00519281').filter(Measurement.date >= '2016-08-23').all()

    session.close()

    active_station = list(np.ravel(active_station))
    return jsonify(active_station)

# Min, Max and Avg 
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def max_avg_min():

# Create our session (link) from Python to the DB
    session = Session(engine)

# Query the most active stations`s date and temperature observations
    active_station= session.query(Measurement.station, Measurement.date, Measurement.tobs).filter_by(station = 'USC00519281').filter(Measurement.date >= '2016-08-23').all()

    session.close()

    active_station = list(np.ravel(active_station))
    return jsonify(active_station)



if __name__ == "__main__":
    app.run(debug=True)
