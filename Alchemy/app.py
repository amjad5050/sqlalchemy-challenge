import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
file_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
db_path = f"sqlite:///{file_dir}/hawaii.sqlite"
print(db_path)
engine = create_engine(db_path)

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
        f"/api/v1.0/<start>/<start>/<end>"
    )




@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    print(results)

    # Convert list of tuples into normal list
    results = list(np.ravel(results))

    print(results[0:2])

    return jsonify(results)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    return jsonify(results)
    
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.tobs).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(most_active=(session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))).all()
    
    session.close()


@app.route("/api/v1.0/<start>/<end>")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(most_active=(session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))
    ).all()

    session.close()


  
    



if __name__ == '__main__':
    app.run(debug=True)




    