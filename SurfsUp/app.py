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
        <font color="blue" size="6"><b>Welcome to the Climate App!</b></font><br><br>
        <font color="red" size="4"><b>Available Routes:</b></font><br>
        <b>/api/v1.0/precipitation</b><br>
        <font color="green"><i>- Returns the date and precipitation data for the last 12 months.</i></font><br><br>
        
        <b>/api/v1.0/stations</b><br>
        <font color="green"><i>- Returns a list of weather stations in the dataset.</i></font><br><br>
        
        <b>/api/v1.0/tobs</b><br>
        <font color="green"><i>- Returns the temperature observations for the most active station for the last 
        12 months.</i></font><br><br>
        
        <b>/api/v1.0/&lt;start&gt;</b><br>
        <font color="green"><i>- Returns the minimum, average, and maximum temperature for all dates greater than 
        or equal to the specified start date (YYYY-MM-DD).</i></font><br><br>
        
        <b>/api/v1.0/&lt;start&gt;/&lt;end&gt;</b><br>
        <font color="green"><i>- Returns the minimum, average, and maximum temperature for dates between the 
        specified start date and end date (YYYY-MM-DD).</i></font><br><br>
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

    # Perform the query to retrieve the list of stations with their IDs and names
    results = session.query(Station.station, Station.name).all()
    
    session.close()

    # Create a list of dictionaries containing station IDs and names
    stations_list = [{"station_id": station[0], "name": station[1]} for station in results]

    # Return the JSON representation of the list
    return jsonify(stations_list)

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
     # Get the station name for the most active station
    most_active_station_name = session.query(Station.name).filter(Station.station == most_active_station_id).first()[0]
    
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station_id, Measurement.date >= one_year_ago_date).all()
        
    session.close()

    # Convert the list of Row objects to a list of dictionaries
    temperature_data_list = [{"date": row[0], "tobs": row[1]} for row in temperature_data]
    
    # Add the station name and ID to the response
    response = {
        "station_id": most_active_station_id,
        "station_name": most_active_station_name,
        "temperatures": temperature_data_list
    }
    
    return jsonify(response)

@app.route('/api/v1.0/<start>')
def temperature_stats_start(start):
    session = Session(engine)
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')

    # Perform the query to calculate TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    # Return a JSON list of temperature statistics for each date
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date - dt.timedelta(days=1)).\
                        group_by(Measurement.date).all()

    session.close()

    if not results:
        return jsonify({"message": "Temperature data not available for the given start date."})
    else:
        temp_stats_list = [{"date": result[0], "TMIN": result[1], "TAVG": result[2], "TMAX": result[3]} for result in results]
        return jsonify(temp_stats_list)

@app.route('/api/v1.0/<start>/<end>')
def temperature_stats_start_end(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert start and end strings to datetime objects
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')

    # Perform the query to calculate TMIN, TAVG, and TMAX for dates from start date to end date (inclusive)
    # Return a JSON list of temperature statistics for each date
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date - dt.timedelta(days=1), Measurement.date <= end_date).\
                        group_by(Measurement.date).all()
    
    session.close()

    # Check if any results are available and handle accordingly
    if not results:
        # If no results are available, return a JSON response with a message
        return jsonify({"message": "Temperature data not available for the given date range."})
    else:
        # If results are available, create a list of temperature statistics for each date
        temp_stats_list = [{"date": result[0], "TMIN": result[1], "TAVG": result[2], "TMAX": result[3]} for result in results]
        return jsonify(temp_stats_list)
    
if __name__ == '__main__':
    app.run(debug=True)
