import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func 
from sqlalchemy import inspect 

from flask import Flask, jsonify

app = Flask(__name__)
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

#assume that we need to return the last year of data from the rain gauge that has the most data 
@app.route("/api/v1.0/precipitation")
def precipitation():
    #set up the data base 
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement 
    session = Session(engine)

    # Find the start of the last year of data 
    end_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    end_date = dt.date(*map(int, end_date_str[0].split('-')))
    start_date = end_date - dt.timedelta(days=365) 
    start_date_str = start_date.strftime("%Y-%m-%d") 
    
    # Get the data 
    max_station = "USC00519397"
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > start_date_str, Measurement.station == max_station).all()
    session.close()
    
    # Append the results to a list of dictionaries 
    prcp_list = []
    for date, prcp in results:
        t_dict = {}
        t_dict["date"] = date
        t_dict["prcp"] = prcp
        prcp_list.append(t_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/station")
def station():
    #set up the data base 
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Station = Base.classes.station 
    session = Session(engine)
    
    #get the station metadata 
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation ).all()
    session.close()

    # Append the results to a list of dictionaries 
    stn_list = []
    for res in results:
        t_dict = {}
        t_dict["station"] = res.station
        t_dict["name"] = res.name
        t_dict["latitude"] = res.latitude
        t_dict["longitude"] = res.longitude
        t_dict["elevation"] = res.elevation
        stn_list.append(t_dict)
    
    return jsonify(stn_list)

if __name__ == '__main__':
    app.run(debug=True)
   