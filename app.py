from flask import Flask, jsonify
import json
from flask import Flask, render_template
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station



app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html", title="SQLAlchemy API Homework with Navigation")

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date,Measurement.prcp).\
                order_by(Measurement.date).all()
    session.close()

    precipitation = list(np.ravel(results))
    precipitation = {precipitation[i]: precipitation[i + 1] for i in range(0, len(precipitation), 2)} 

    return render_template('index2.html', jsonfile=json.dumps(precipitation))

@app.route("/api/v1.0/precipitation2")
def precipitation2():
    session = Session(engine)

    results = session.query(Measurement.date,Measurement.prcp).\
                order_by(Measurement.date).all()
    session.close()

    precipitation = list(np.ravel(results))
    precipitation = {precipitation[i]: precipitation[i + 1] for i in range(0, len(precipitation), 2)} 

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).\
                 order_by(Station.station).all()

    session.close()

    stations = list(np.ravel(results))

    return render_template('index2.html', jsonfile=json.dumps(stations))

@app.route("/api/v1.0/stations2")
def stations2():
    session = Session(engine)

    results = session.query(Station.station).\
                 order_by(Station.station).all()

    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date,  Measurement.tobs).\
            filter(Measurement.date >= '2016-08-23').\
                 order_by(Measurement.date).all()

    session.close()

    tobs = list(np.ravel(results))

    tobs = {tobs[i]: tobs[i + 1] for i in range(0, len(tobs), 2)} 

    return render_template('index2.html', jsonfile=json.dumps(tobs))

@app.route("/api/v1.0/tobs2")
def tobs2():
    session = Session(engine)

    results = session.query(Measurement.date,  Measurement.tobs).\
            filter(Measurement.date >= '2016-08-23').\
                 order_by(Measurement.date).all()

    session.close()

    tobs = list(np.ravel(results))

    tobs = {tobs[i]: tobs[i + 1] for i in range(0, len(tobs), 2)} 

    return jsonify(tobs)

@app.route("/api/v1.0/<start_date>")
def data_start_date(start_date):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

    session.close()

    start_date = []
    for min, avg, max in results:
        start_date2 = {}
        start_date2["Minimum_Temp"] = min
        start_date2["AVG_Temp"] = avg
        start_date2["Max_Temp"] = max
        start_date.append(start_date2) 
    
    return jsonify(start_date)

@app.route("/api/v1.0/<start_date>/<end_date>")
def data_start_end_date(start_date, end_date):
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    end_date = []
    for min, avg, max in results:
        end_date2 = {}
        end_date2["Minimum_Temp"] = min
        end_date2["AVG_Temp"] = avg
        end_date2["Max_Temp"] = max
        end_date.append(end_date2) 
    

    return jsonify(end_date)

if __name__ == "__main__":
    app.run(debug=True)