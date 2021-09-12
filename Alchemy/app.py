import datetime as dt
import numpy as np
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
###file_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
###db_path = f"sqlite:///{file_dir}/hawaii.sqlite"
###print(db_path)
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

# Save reference to the table
Measurement = Base.classes.measurement
Station=Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Homepage:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )




@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)    
    results = session.query(Measurement.date,Measurement.prcp)
    filter(Measurement.date >= prev_year).all()

    
    ##print(results)

    # Convert list of tuples into normal list
    results = {date: prcp for date, prcp in prcp
    }

    return jsonify(results)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()
    stations = list(np.ravel(results))
    return jsonify(results)
    
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)


    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).\
        all()

    session.close()
    temps = list(np.ravel(results))

    return jsonify(temps=temps)

@app.route("/api/v1.0/<start>")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start = dt.datetime.strptime(start, "%m%d%Y")
    results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start)
    start = dt.datetime.strptime(start, "%m%d%Y")
    results1 = session.query(results).\
              filter(Measurement.date >= start).\
              all()

    session.close()

    temps = list(np.ravel(results1))
    return jsonify(temps)

    session.close()
    return jsonify(results)



@app.route("/api/v1.0/<start>/<end>")
def end():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= stop).all()
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    all()

    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)



if __name__ == '__main__':
    app.run(debug=True)




    