# sqlalchemy-challenge
Module 10 Challenge - Advanced SQL

Before going on long holiday vacation in Honolulu, Hawaii, to help with trip planning, a climate analysis about the area is performed. 

Repository Folders and Contents:
- SurfsUp:
  - Resources:
    - hawaii.sqlite
    - hawaii_measurements.csv
    - hawaii_stations.csv
  - app.py
  - climate_kt.ipynb

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Installing](#installing)

## About
**Part 1: Analyse and Explore the Climate Data**

Python and SQLAlchemy are used to do a basic climate analysis and data exploration of the climate database. Specifically, SQLAlchemy ORM queries, Pandas, and Matplotlib.ct are used.

Tools/Libraries Imported:
- matplotlib.pyplot library: used for creating graphs and charts
- matplotlib style 'fivethirtyeight': specific plot style with predefined colours, and fonts
- numpy library: used for numerical computations
- pandas library: used for data manipulation and analysis
- datetime library: provides classes for manipulating dates and times
- sqlachemy toolkit:
  - sqlalchemy library: provides the SQL toolkit and Object-Relational Mapper (ORM) functionality
  - sqlalchemy.ext.automap module and automap_base function: to reflect an existing database schema and generate Python classes that represent the database tables
  - sqlalchemy.orm module and Session class: the Session class is used to interact with the database and perform Create, Read, Update and Delect (CRUD) operations. 

Jupyter Notebook Python Script:
- File: climate_kt.ipynb
- Purpose:
  - Use sqlalchemy to connect to the hawaii.sqlite database
  - Reflect the tables from the database into classes and save references to them, named 'station' and 'measurement'
  - link Python to the hawaii.sqlite database by creating a sqlalchemy session
  - perform a precipation analysis:
    - find the most recent 12 months of data from the dataset
    - select only the date and precipitation (prcp) values
    - load these values into a Pandas DataFrame
    - sort the datafram by date
    - plot the results in a line chart, with date on the x-axis and precipitation on the y-axis
    - use Pandas to calculate the summary statistics for the precipitation data
   - perform a station analysis:
    - calculate the total number of stations in the dataset
    - work out the most-active stations by listing the stations and observation counts in descending order
    - once identifying the most active station ie. most observations, filter to the previous 12 months of data
    - create a histogram of this data in 12 bins
  

**Part 2: Design a Climate App**

A Flask API was designed based on the queries that were developed in Part 1. 

Tools/Libraries Imported:
- flask library with flask and jsonify modules:  Flask class to create web applications and jsonify to convert python to JSON format
- datetime library: provides classes for manipulating dates and times
- sqlachemy toolkit:
  - sqlalchemy library: provides the SQL toolkit and Object-Relational Mapper (ORM) functionality
  - sqlalchemy.ext.automap module and automap_base function: to reflect an existing database schema and generate Python classes that represent the database tables
  - sqlalchemy.orm module and Session class: the Session class is used to interact with the database and perform Create, Read, Update and Delect (CRUD) operations.
  - sqlalchemy create_engine function: to create a database engine to connect with the database in order to interact with the database, and perform operations such as SQL queries
  - sqlalchemy func object: to build SQL expressions and perform database operations such as aggregations ie. count, sum, avg

Visual Studio Code Python Script:
- File: app.py
- Purpose:
  - Use sqlalchemy to connect to the hawaii.sqlite database
  - Reflect the tables from the database into classes and save references to them, named 'station' and 'measurement'
  - Define the routes in the flask app, that will show json responses with climate data:
    - '/': the homepage route, with welcome message and a list the available routes
    - 'api/v1.0/precipitation': returns the date and precipitation data for the last 12 months
    - 'api/v1.0/stations': returns a list of weather stations in the dataset
    - 'api/v1.0/tobs': returns the temperature observations for the most active station for the last 
        12 months
    - 'api/v1.0/<start>': returns the minimum, average, and maximum temperature for all dates greater than 
        or equal to the specified start date (YYYY-MM-DD)
    - 'api/v1.0/<start>/<end>': returns the minimum, average, and maximum temperature for dates between the 
        specified start date and end date (YYYY-MM-DD)
  - Add code to run the web application, this is so that a client can make a HTTP request to API endpoints, the server retrieves the data from the hawaii.sqlite database, processes it and returns a JSON format result.


## Getting Started
To open climate_kt.ipynb in Juypter Notebook:
  - Open Anaconda Prompt
  - Activate dev environment type 'conda activate dev'
  - Navigate to the folder where repository is saved on local drive
  - Open Jupyter Notebook type 'Jupyter Notebook'

To open and activate the flask API:
 - Open in app.py in Visual Studio Code
 - Navigate to the folder location of the app.py file where it is saved on the local drive
 - In the Terminal type 'python app.py'
 - The url should be http://127.0.0.1:5000:
  - open a webpage with the above url
  - add the different routes to see the JSON output eg. http://127.0.0.1:5000/api/v1.0/precipitation
  - to close the flask app in Visual Studio Code, press Ctrl + c

## Installing
Flask needs to be installed in order to run Flask API.
To check if it is installed, in Anaconda Prompt type 'conda install -c anaconda flask'.
To check which version of flask has been installed, type 'flask --version'.




