import numpy as np
import pandas as pnd
import geopandas as gp
import requests
import json
import geojson
import csv
import time
import pathlib
import polyline
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape
from shapely.geometry import asShape
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

current_folder = pathlib.Path(__file__).parent.absolute()
engine = create_engine('postgresql+psycopg2:///city_bikes', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# Find all unique routes in the ride data, query the Project OSRM API and save the results to table "route" in the database and to a json file
base_URL = "http://router.project-osrm.org/route/v1/bike/"
PARAMS = {'alternatives': 'false', 'steps': 'false', 'geometries': 'geojson', 'overview': 'full', 'annotations': 'false'}
session = Session()
# sql_query = "SELECT DISTINCT r.departure_station_id, s1.latitude AS departure_lat, s1.longitude AS departure_long, r.return_station_id, s2.latitude AS return_lat, s1.longitude AS return_long FROM ride AS r JOIN station AS s1 ON r.departure_station_id = s1.station_id JOIN station AS s2 ON r.return_station_id = s2.station_id;"
# comb = session.execute(sql_query).fetchall()
# print("Writing unique routes to csv for future use.")
# with open('ainutkertaiset_reitit.csv', 'w') as outfile:
#       newFileWriter = csv.writer(outfile) 
#       for r in comb:
#         newFileWriter.writerow(r)
comb = []
with open('ainutkertaiset_reitit_2.csv', 'r') as infile:
  newFileReader = csv.reader(infile) 
  for row in newFileReader:
    comb.append(row)
routes = [['start_id', 'finish_id', 'distance', 'duration', 'geometry']]
totalcount = str(len(comb))
print(totalcount)
counter = 0
# Definitions for the Route and Ride classes
class Route(Base):
        __tablename__ = 'route'
        id = Column(Integer, primary_key=True)
        start_id = Column(Integer)
        finish_id = Column(Integer)
        distance = Column(Numeric)
        duration = Column(Numeric)
        geom = Column(Geometry('LINESTRING'))
        rides = relationship('Ride')

class Ride(Base):
        __tablename__ = 'ride'
        id = Column(Integer, primary_key=True)
        departure_time = Column(DateTime)
        return_time = Column(DateTime)
        departure_station_id = Column(String)
        return_station_id = Column(String)
        distance = Column(Numeric)
        duration = Column(Numeric)
        route_id = Column(Integer, ForeignKey('route.id'))

# Setting retry parameters
s = rq.Session()
retries = Retry(total=5,
                backoff_factor=1,
                status_forcelist=[ 500, 502, 503, 504 ])
s.mount('http://', HTTPAdapter(max_retries=retries))
start_time = time.perf_counter()
for row in comb:
  coordinates = str(row[1]) + ',' + str(row[2]) + ';' + str(row[4]) + ',' + str(row[5])
  print(coordinates)
  URL = base_URL + coordinates
  request = s.get(url = URL, params = PARAMS)
  json_geometry = request.json()['routes'][0]['geometry']
  distance = request.json()['routes'][0]['distance']
  duration = request.json()['routes'][0]['duration']
  routes.append([row[0], row[3], distance, duration,json_geometry])
  geojson_geom = geojson.loads(json.dumps(json_geometry))
  geometry = from_shape(asShape(geojson_geom), srid=3857)
  route = Route(start_id=row[0], finish_id=row[3], distance=distance, duration=duration, geom=geometry)
  session.add(route)
  counter = counter + 1


  if counter % 10 == 0:
    current_time = time.perf_counter()
    print("Writing to csv at "  + str(current_time - start_time) + " seconds")
    with open('reitit_asemien_välillä.csv', 'a') as outfile:
      newFileWriter = csv.writer(outfile) 
      for r in routes:
        newFileWriter.writerow(r)
    print("Written to csv at "  + str(current_time - start_time) + " seconds")
    routes = []
    session.commit()
    session.flush()
    current_time = time.perf_counter()
    print("Saved " + str(counter) + " / " + totalcount + " routes in " + str(current_time - start_time) + " seconds.")
with open('reitit_asemien_välillä.csv', 'a') as outfile:
  newFileWriter = csv.writer(outfile) 
  for r in routes:
    newFileWriter.writerow(r)
session.commit()
current_time = time.perf_counter()
print("Saved " + str(counter) + " / " + totalcount + " routes in " + str(current_time - start_time) + "seconds.")
