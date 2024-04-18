# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from datetime import datetime, timedelta


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


 
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of your dictionary."""
    # Calculate the date one year from the last date in data set
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_date - timedelta(days=365)
    
    # Query precipitation data for the last 12 months
    precipitation_data = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= one_year_ago)\
        .order_by(Measurement.date).all()
    
    # Convert to dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # Query stations
    stations = session.query(Station.station).all()
    
    # Convert to list
    station_list = list(np.ravel(stations))
    
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the previous year."""
    # Find the most active station
    active_stations = session.query(Measurement.station, func.count(Measurement.station))\
        .group_by(Measurement.station)\
        .order_by(desc(func.count(Measurement.station)))\
        .first()
    
    most_active_station_id = active_stations[0]
    
    # Calculate the date one year from the last date in data set
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_date - timedelta(days=365)
    
    # Query temperature data for the last 12 months for the most active station
    temperature_data = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active_station_id)\
        .filter(Measurement.date >= one_year_ago)\
        .order_by(Measurement.date).all()
    
    # Convert to list of dictionaries
    temperature_list = [{"Date": date, "Temperature": temp} for date, temp in temperature_data]
    
    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>")
def calc_temps_start(start):
    """Return a JSON list of the minimum temperature, average temperature, and maximum temperature for a specified start date."""
    # Query to calculate TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .all()
        # .group_by(Measurement.date)\

    # Convert the results to a list of dictionaries
    
    # temp_data = []
    # for result in results:
    #     temp_data.append({
    #         "Date": result[0],
    #         "Minimum Temperature": result[1],
    #         "Average Temperature": result[2],
    #         "Maximum Temperature": result[3]
    #     })
    
    temp_data = {
        "Start Date": start,
        "Minimum Temperature": results[0][1],
        "Average Temperature": results[0][2],
        "Maximum Temperature": results[0][3]
    }

    return jsonify(temp_data)
    
@app.route("/api/v1.0/<start>/<end>")
def calc_temps_start_end(start, end):
    """Return a JSON list of the minimum temperature, average temperature, and maximum temperature for a specified start-end range."""
    # Query to calculate TMIN, TAVG, and TMAX for dates between start date and end date (inclusive)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end)\
        .all()
        # .group_by(Measurement.date)\

    # Convert the results to a list of dictionaries
    temp_data = {
        "Start Date": start,
        "End Date": end,
        "Minimum Temperature": results[0][1],
        "Average Temperature": results[0][2],
        "Maximum Temperature": results[0][3]
    }

    return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)