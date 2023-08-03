from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Create a Flask app
app = Flask(__name__)

# Set up the database connection to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# reflect the tables
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Define the routes
@app.route('/')
def homepage():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """List all available API routes with descriptions."""
    return """
        Welcome to the Climate App!<br><br>
        Available Routes:<br>
        <b>/api/v1.0/precipitation</b><br>
        - Returns the date and precipitation data for the last 12 months.<br><br>
        
        <b>/api/v1.0/stations</b><br>
        - Returns a list of weather stations in the dataset.<br><br>
        
        <b>/api/v1.0/tobs</b><br>
        - Returns the temperature observations for the most active station for the last 12 months.<br><br>
        
        <b>/api/v1.0/&lt;start&gt;</b><br>
        - Returns the minimum, average, and maximum temperature for all dates greater than or equal to the specified start date (YYYY-MM-DD).<br><br>
        
        <b>/api/v1.0/&lt;start&gt;/&lt;end&gt;</b><br>
        - Returns the minimum, average, and maximum temperature for dates between the specified start date and end date (YYYY-MM-DD).<br><br>
    """


@app.route('/api/v1.0/precipitation')
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in the data set.
    most_recent_date = session.query(func.max(Measurement.date)).first()
    most_recent_date = dt.datetime.strptime(most_recent_date[0], '%Y-%m-%d')
    one_year_ago_date = most_recent_date - dt.timedelta(days=366)

    # Perform the query to retrieve the date and precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago_date).all()
    
    session.close()
    
    # Convert the query results to a dictionary with date as the key and prcp as the value
    precipitation_data = {date: prcp for date, prcp in results}

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform the query to retrieve the list of stations
    # Return a JSON list of stations
    results = session.query(Station.station).all()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)
    
    session.close()

@app.route('/api/v1.0/tobs')
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Calculate the date one year from the last date in the data set.
    most_recent_date = session.query(func.max(Measurement.date)).first()
    most_recent_date = dt.datetime.strptime(most_recent_date[0], '%Y-%m-%d')
    one_year_ago_date = most_recent_date - dt.timedelta(days=366)

    # Perform the query to retrieve the temperature observations of the most active station for the last 12 months
    # Return a JSON list of temperature observations for the previous year
    # Design a query to find the most active stations (i.e. which stations have the most rows?)
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    # List the stations and their counts in descending order.
    active_stations_list = []

    for row in active_stations:
        active_stations_list.append((row[0], row[1]))

    active_stations_list = sorted(active_stations_list, key=lambda x: x[1], reverse=True)

    most_active_station_id = active_stations[0][0]
    temperature_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station_id, Measurement.date >= one_year_ago_date).all()
        
    session.close()

    # Convert the list of Row objects to a list of dictionaries
    temperature_data_list = [{"date": row[0], "tobs": row[1]} for row in temperature_data]
    
    return jsonify(temperature_data_list)

@app.route('/api/v1.0/<start>')
def temperature_stats_start(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert start string to datetime object
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    
    # Perform the query to calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
    # Return a JSON list of the minimum temperature, average temperature, and maximum temperature

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date).all()
    
    session.close()

    # Check if any of the results are None and handle accordingly
    if None in results[0]:
        # If any of the values are None, return a JSON response with a message
        return jsonify({"message": "Temperature data not available for the given start date."})
    else:
        # If all values are available, return the temperature statistics as JSON
        temp_stats = {"TMIN": results[0][0], "TAVG": results[0][1], "TMAX": results[0][2]}
        return jsonify(temp_stats)

@app.route('/api/v1.0/<start>/<end>')
def temperature_stats_start_end(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert start and end strings to datetime objects
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')

    # Perform the query to calculate TMIN, TAVG, and TMAX for dates from start date to end date (inclusive)
    # Return a JSON list of the minimum temperature, average temperature, and maximum temperature

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    
    session.close()

    # Check if any of the results are None and handle accordingly
    if None in results[0]:
        # If any of the values are None, return a JSON response with a message
        return jsonify({"message": "Temperature data not available for the given date range."})
    else:
        # If all values are available, return the temperature statistics as JSON
        temp_stats = {"TMIN": results[0][0], "TAVG": results[0][1], "TMAX": results[0][2]}
        return jsonify(temp_stats)

if __name__ == '__main__':
    app.run(debug=True)
