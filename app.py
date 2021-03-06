# Import everything you used in the starter_climate_analysis.ipynb file, along with Flask modules


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

#################################################
# Database Setup
#################################################
# Create an engine
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model with automap_base() and Base.prepare()
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Instantiate a Session and bind it to the engine
session = Session(engine)

#################################################
# Flask Setup
#################################################

# Instantiate a Flask object at __name__, and save it to a variable called app
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Set the app.route() decorator for the base '/'
@app.route("/")
# define a welcome() function that returns a multiline string message to anyone who visits the route
def welcome():

    return(
    f"Welcome to this painful Hawaii API<br/>"
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/temp/start/end"
)
    
# Set the app.route() decorator for the "/api/v1.0/precipitation" route
@app.route("/api/v1.0/precipitation")

# define a precipitation() function that returns jsonified precipitation data from the database
def precipitation():

# In the function (logic should be the same from the starter_climate_analysis.ipynb notebook):
    # Calculate the date 1 year ago from last date in database
    # end_date = (session.query(measurement.date).filter(measurement.date.desc()).first())
    
    


    # end_date_formatted = dt.date(2017, 8, 23)
    # target_date = (end_date_formatted - dt.timedelta(days=365))
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query for the date and precipitation for the last year
    precipitation = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= prev_year).all()

    # Create a dictionary to store the date: prcp pairs. 
    # Hint: check out a dictionary comprehension, which is similar to a list comprehension but allows you to create dictionaries
    prciptn = {date: prcp for date, prcp in precipitation}
    # Return the jsonify() representation of the dictionary
    return jsonify(prciptn)

# Set the app.route() decorator for the "/api/v1.0/stations" route
@app.route("/api/v1.0/stations")


# define a stations() function that returns jsonified station data from the database
def stations():
    
    results = session.query(station.station).all()
    
# In the function (logic should be the same from the starter_climate_analysis.ipynb notebook):
    # Query for the list of stations

    # Unravel results into a 1D array and convert to a list
    # Hint: checkout the np.ravel() function to make it easier to convert to a list
    stations = list(np.ravel(results))
    return jsonify(stations)
    # Return the jsonify() representation of the list


# Set the app.route() decorator for the "/api/v1.0/tobs" route
# define a temp_monthly() function that returns jsonified temperature observations (tobs) data from the database
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# In the function (logic should be the same from the starter_climate_analysis.ipynb notebook):
    # Calculate the date 1 year ago from last date in database
    # target_date = (end_date_formatted - dt.timedelta(days=365))

    # Query the primary station for all tobs from the last year
    results = session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= prev_year).all()

    # Unravel results into a 1D array and convert to a list
    # Hint: checkout the np.ravel() function to make it easier to convert to a list
    temps = list(np.ravel(results))

    # Return the jsonify() representation of the list
    return jsonify(temps)

# Set the app.route() decorator for the "/api/v1.0/temp/<start>" route and "/api/v1.0/temp/<start>/<end>" route
# define a stats() function that takes a start and end argument, and returns jsonified TMIN, TAVG, TMAX data from the database
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):

    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

    # If the end argument is None:
        # calculate TMIN, TAVG, TMAX for dates greater than start
    if not end:
        results = session.query(*sel).\
        filter(measurement.date >= start).all()
        # Unravel results into a 1D array and convert to a list
        # Hint: checkout the np.ravel() function to make it easier to convert to a list
        temps = list(np.ravel(results))
        # Return the jsonify() representation of the list
        return jsonify(temps)
    # Else:
        # calculate TMIN, TAVG, TMAX with both start and stop
    results = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()

        # Unravel results into a 1D array and convert to a list
        # Hint: checkout the np.ravel() function to make it easier to convert to a list
    temps = list(np.ravel(results))
        
        # Return the jsonify() representation of the list
    return jsonify(temps)

if __name__ == '__main__':
    app.run()
