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
from decimal import Decimal

current_folder = pathlib.Path(__file__).parent.absolute()
engine = create_engine('postgresql+psycopg2:///city_bikes', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# Find all unique routes in the ride data, query the Project OSRM API and save the results to table "route" in the database and to a json file
url = 'https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql'
headers = { "Content-Type": "application/graphql" }
session = Session()
comb = []
with open('toinen_kierros.csv', 'r') as infile:
  newFileReader = csv.reader(infile) 
  for row in newFileReader:
    comb.append(row)
routes = [['start_id', 'finish_id', 'distance', 'duration', 'geometry']]
totalcount = str(len(comb))
print(totalcount)
counter = 0
# Definitions for the Route and Ride classes
class GeoRoute(Base):
        __tablename__ = 'geo_route'
        id = Column(Integer, primary_key=True)
        start_id = Column(Integer)
        finish_id = Column(Integer)
        distance = Column(Numeric)
        duration = Column(Numeric)
        geom = Column(Geometry('LINESTRING'))
# GeoRoute.__table__.create(engine)

# Setting retry parameters
s = requests.Session()
retries = Retry(total=5,
                backoff_factor=1,
                status_forcelist=[ 500, 502, 503, 504 ])
s.mount('http://', HTTPAdapter(max_retries=retries))
start_time = time.perf_counter()
for row in comb:
  coordinates = str(row[1]) + ',' + str(row[2]) + ';' + str(row[4]) + ',' + str(row[5])
  
  body = '{plan(fromPlace: "::' + str(row[1]) + ',' + str(row[2]) + '", toPlace: "::' + str(row[4]) + ',' + str(row[5]) + '", numItineraries: 1, transportModes: {mode: BICYCLE}) {itineraries{duration legs {distance legGeometry {length points}}}}}'
  request = requests.post(url, data = body, headers = headers)
  if ('data' in request.json()) and (len(request.json()['data']['plan']['itineraries']) > 0): 
    itinerary = request.json()['data']['plan']['itineraries'][0]
    duration = itinerary['duration']
    distance = 0
    points = []
    for leg in itinerary['legs']:
      distance = distance + leg['distance']
      for point in polyline.decode(leg['legGeometry']['points']):
        if len(points) == 0 or point != points[-1]:
          points.append(point)
    json_geometry = {'type': 'LineString', 'coordinates': []}
    for point in points: 
      y = point[0]
      x = point[1]
      coord = []
      coord.append(y)
      coord.append(x)
      json_geometry['coordinates'].append(coord)
    routes.append([row[0], row[3], distance, duration, json_geometry])
    geojson_geom = geojson.loads(json.dumps(json_geometry))
    geometry = from_shape(asShape(geojson_geom), srid=3857)
    geo_route = GeoRoute(start_id=row[0], finish_id=row[3], distance=distance, duration=duration, geom=geometry)
    session.add(geo_route)
  else:
    if row[0] == row[3]:
      json_geometry = {'type': 'LineString', 'coordinates': [[row[1], row[2]] ,[row[4], row[5]]]}
      routes.append([row[0], row[3], '0', '0', json_geometry])  
    else:
      routes.append([row[0], row[3], '0', '0', '{}'])
  counter = counter + 1
  if counter % 10 == 0:
    current_time = time.perf_counter()
    with open('reitit_asemien_välillä.csv', 'a') as outfile:
      newFileWriter = csv.writer(outfile) 
      for r in routes:
        newFileWriter.writerow(r)
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
