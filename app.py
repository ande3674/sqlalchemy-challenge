from flask import Flask, render_template, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Create database connection with auto mapped classes using SQLAlchemy
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


# Start Flask app
app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query precipitation
    last_year_rows = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date >= '2016-08-23') \
                            .order_by(Measurement.date.asc()).all()

    #Convert the query results to a dictionary using date as the key and prcp as the value.
    prcp_dict = {}
    for row in last_year_rows:
        prcp_dict[row.date] = row.prcp

    #Return the JSON representation of your dictionary.
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    session_rows = session.query(Station).all()
    return_string = "All Stations: <br>"
    for row in session_rows:
        return_string += f"{row.name} <br>"
    return return_string


@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active station for the last year of data.

    # Return a JSON list of temperature observations (TOBS) for the previous year.

    return ""



if __name__ == "__main__":
    app.run(debug=True)