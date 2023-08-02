from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Create a Flask app
app = Flask(__name__)

# Set up the database connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Define the routes
@app.route('/')
def homepage():
    return "Welcome to the Climate App. Available routes: /api/v1.0/precipitation, /api/v1.0/stations, /api/v1.0/tobs, /api/v1.0/&lt;start&gt;, /api/v1.0/&lt;start&gt;/&lt;end&gt;"

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Calculate the date one year from the last date in the data set.
    most_recent_date = session.query(func.max(Measurement.date)).first()
    most_recent_date = dt.datetime.strptime(most_recent_date[0], '%Y-%m-%d')
    one_year_ago_date = most_recent_date - dt.timedelta(days=366)

    # Perform the query to retrieve the date and precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago_date).all()

    # Convert the query results to a dictionary with date as the key and prcp as the value
    precipitation_data = {date: prcp for date, prcp in results}

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    # Perform the query to retrieve the list of stations
    # Return a JSON list of stations
    with Session() as session:
        results = session.query(Station.station).all()
        stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    # Perform the query to retrieve the temperature observations of the most active station for the last 12 months
    # Return a JSON list of temperature observations for the previous year

    most_active_station_id = active_stations[0][0]
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station_id, Measurement.date >= one_year_ago_date).all()
    tobs_data = {date: tobs for date, tobs in results}
    return jsonify(tobs_data)

@app.route('/api/v1.0/<start>')
def temperature_stats_start(start):
    # Perform the query to calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
    # Return a JSON list of the minimum temperature, average temperature, and maximum temperature

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).all()
    temp_stats = {"TMIN": results[0][0], "TAVG": results[0][1], "TMAX": results[0][2]}
    return jsonify(temp_stats)

@app.route('/api/v1.0/<start>/<end>')
def temperature_stats_start_end(start, end):
    # Perform the query to calculate TMIN, TAVG, and TMAX for dates from start date to end date (inclusive)
    # Return a JSON list of the minimum temperature, average temperature, and maximum temperature

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start, Measurement.date <= end).all()
    temp_stats = {"TMIN": results[0][0], "TAVG": results[0][1], "TMAX": results[0][2]}
    return jsonify(temp_stats)

if __name__ == '__main__':
    app.run(debug=True)
