import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func 
from sqlalchemy import inspect 

from flask import Flask, json, jsonify

app = Flask(__name__)
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<'start_date'> <br>"
        f"/api/v1.0/<'start_date'>/<'end_date'>"
    )

#assume that we need to return the last year of data from the rain gauge that has the most data 
@app.route("/api/v1.0/precipitation")
def precipitation():
    #set up the data base 
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement 
    Station = Base.classes.station
    session = Session(engine)

    # Find the start of the last year of data 
    end_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    end_date = dt.date(*map(int, end_date_str[0].split('-')))
    start_date = end_date - dt.timedelta(days=365) 
    start_date_str = start_date.strftime("%Y-%m-%d") 
    
    # Find the station with the most observations 
    number_days = session.query(Measurement.station, func.count(Measurement.prcp)).group_by(Measurement.station).order_by(func.count(Measurement.prcp).desc()).all()
    max_station = number_days[0][0]

    # Get the prcp data for this station 
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > start_date_str, Measurement.station == max_station).all()
    
    # Append the results to a list of dictionaries 
    prcp_list = []
    for date, prcp in results:
        t_dict = {}
        t_dict["date"] = date
        t_dict["prcp"] = prcp
        prcp_list.append(t_dict)

    # Get the metadata for this station  
    stn_results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation ).filter(Station.station == max_station).all()
    session.close()

    # Append the results to a list of dictionaries 
    stn_list = []
    for res in stn_results:
        t_dict = {}
        t_dict["station"] = res.station
        t_dict["name"] = res.name
        t_dict["latitude"] = res.latitude
        t_dict["longitude"] = res.longitude
        t_dict["elevation"] = res.elevation
        t_dict["variable"] = "Daily rainfall accumulation (Inch)"
        stn_list.append(t_dict)

    # make a list of lists and return 
    results_list = []
    results_list.append(stn_list)
    results_list.append(prcp_list)
    return jsonify(results_list)

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

@app.route("/api/v1.0/tobs")
def tobs():
    #set up the data base 
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement 
    Station = Base.classes.station
    session = Session(engine)

    # Find the start of the last year of data 
    end_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    end_date = dt.date(*map(int, end_date_str[0].split('-')))
    start_date = end_date - dt.timedelta(days=365) 
    start_date_str = start_date.strftime("%Y-%m-%d") 
    
    # Find the station with the most observations 
    number_days = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).all()
    max_station = number_days[0][0]
    
    # Get the data for this station 
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > start_date_str, Measurement.station == max_station).all()
   
    # Append the results to a list of dictionaries 
    tobs_list = []
    for date, tobs in results:
        t_dict = {}
        t_dict["date"] = date
        t_dict["tobs"] = tobs
        tobs_list.append(t_dict)

    # Get the metadata for this station  
    stn_results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation ).filter(Station.station == max_station).all()
    session.close()

    # Append the results to a list of dictionaries 
    stn_list = []
    for res in stn_results:
        t_dict = {}
        t_dict["station"] = res.station
        t_dict["name"] = res.name
        t_dict["latitude"] = res.latitude
        t_dict["longitude"] = res.longitude
        t_dict["elevation"] = res.elevation
        t_dict["variable"] = "Daily max temp (F)"
        stn_list.append(t_dict)

    # make a list of lists and return 
    results_list = []
    results_list.append(stn_list)
    results_list.append(tobs_list)
    return jsonify(results_list)

@app.route("/api/v1.0/<start_date>")
def get_from_date(start_date):

    # check if valid start_date string 
    try:
        dt.datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        return jsonify("Incorrect date format, should be YYYY-MM-DD")

    #set up the data base 
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement 
    
    #make the queries 
    session = Session(engine)
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    mean_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()

    results_dict = {"min_temp":min_temp,"max_temp":max_temp, "mean_temp":mean_temp}
    return jsonify(results_dict)

@app.route("/api/v1.0/<start_date>/<end_date>")
def get_from_to_date(start_date, end_date):
    # check if valid start date string 
    try:
        dt.datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        return jsonify("Incorrect start date format, should be YYYY-MM-DD")

    # check if valid end date string 
    try:
        dt.datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify("Incorrect end date format, should be YYYY-MM-DD")

    #set up the data base 
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement 
    
    #make the queries 
    session = Session(engine)
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date,Measurement.date <= end_date).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date,Measurement.date <= end_date).all()
    mean_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date,Measurement.date <= end_date).all()
    session.close()

    results_dict = {"min_temp":min_temp,"max_temp":max_temp, "mean_temp":mean_temp}
    return jsonify(results_dict)

    return

if __name__ == '__main__':
    app.run(debug=True)
   