from flask import Flask, render_template
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


# Start Flask app
app = Flask(__name__)

@app.route("/")
def home():
    # List available routes
    routes = "/api/v1.0/precipitation <br>" + \
            "/api/v1.0/stations <br>" + \
            "/api/v1.0/tobs <br>" + \
            "/api/v1.0/<start> <br>" + \
            "/api/v1.0/<start>/<end> <br>"
    return f"Available Routes: <br> {routes}"

if __name__ == "__main__":
    app.run(debug=True)