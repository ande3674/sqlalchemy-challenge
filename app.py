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
    prcp_data = []
    for row in last_year_rows:
        d = {}
        d["date"] = row.date 
        d["prcp"] = row.prcp
        prcp_data.append(d)

    #Return the JSON representation of your dictionary.
    #return jsonify(prcp_dict)
    return render_template('precipitation.html', data=prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    session_rows = session.query(Station).all()
    station_data_list = []
    for row in session_rows:
        d = {}
        d["station"] = row.name
        station_data_list.append(d)
    return render_template('stations.html', data=station_data_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active station for the last year of data.
    last_year_tobs_rows = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= '2016-08-23') \
                            .order_by(Measurement.date.asc()).all()

    tobs_data_list = []

    for row in last_year_tobs_rows:
        d = {}
        d["temp"] = row.tobs
        d["date"] = row.date
        tobs_data_list.append(d)

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    return render_template('temperature.html', data=tobs_data_list)


@app.route("/api/v1.0/<start>")
def start_only(start):
    lowest_temp = session.query(func.min(Measurement.tobs)) \
                        .filter(Measurement.station == 'USC00519281').filter(Measurement.date >= start).all()
    highest_temp = session.query(func.max(Measurement.tobs)) \
                        .filter(Measurement.station == 'USC00519281').filter(Measurement.date >= start).all()
    avg_temp = session.query(func.avg(Measurement.tobs)) \
                        .filter(Measurement.station == 'USC00519281').filter(Measurement.date >= start).all()

    # calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    [(lowest_temp,)] = lowest_temp
    [(highest_temp,)] = highest_temp
    [(avg_temp,)] = avg_temp

    # Return a JSON list of the minimum temperature, the average temperature, and the max 
    # temperature for the given start range.
    return render_template('range.html', min=lowest_temp, max=highest_temp, avg=avg_temp)


@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start, end):
    lowest_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.station == 'USC00519281') \
                        .filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    highest_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.station == 'USC00519281') \
                        .filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00519281') \
                        .filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date, less than end date.
    [(lowest_temp,)] = lowest_temp
    [(highest_temp,)] = highest_temp
    [(avg_temp,)] = avg_temp

    # Return a JSON list of the minimum temperature, the average temperature, and the max 
    # temperature for the given range.
    return render_template('range.html', min=lowest_temp, max=highest_temp, avg=avg_temp)



if __name__ == "__main__":
    app.run(debug=True)