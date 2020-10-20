import numpy as np
import pandas as pnd
import geopandas as gp
import requests as rq
import json
import geojson
import csv
import pathlib
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

current_folder = pathlib.Path(__file__).parent.absolute()
main_folder = current_folder.parent
training_data_folder = main_folder / 'training_data'
data_folder = main_folder / 'data'
work_folder = main_folder / 'workfiles'

url = 'https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql'
headers = { "Content-Type": "application/graphql" }
print("Importing files...")
routes = pnd.read_csv(work_folder / 'district_pairs_pred.csv')
centroids = gp.read_file(data_folder / 'Base_district_centroids_edited.geojson')
print("Converting crs...")
centroids = centroids.to_crs("EPSG:4326")
centroids['tunnus'] = pnd.to_numeric(centroids['tunnus'])
print("Merging data...")
routes = routes.merge(centroids, left_on="start", right_on="tunnus")
routes.drop(['tietopalvelu_id', 'aluejako', 'tunnus', 'nimi_fi','nimi_se','tyyppi','pa','paivitetty_tietopalveluun'], axis=1, inplace=True)
routes = gp.GeoDataFrame(routes)
routes['start_lon'] = routes['geometry'].x
routes['start_lat'] = routes['geometry'].y
routes.drop(['geometry'], axis=1, inplace=True)
routes = routes.merge(centroids, left_on="end", right_on="tunnus")
routes.drop(['tietopalvelu_id', 'aluejako', 'tunnus', 'nimi_fi','nimi_se','tyyppi','pa','paivitetty_tietopalveluun'], axis=1, inplace=True)
routes['end_lon'] = routes['geometry'].x
routes['end_lat'] = routes['geometry'].y
routes.drop(['geometry'], axis=1, inplace=True)
routes = routes.sort_values(['start', 'end'], ignore_index=True)

print("Starting connection...")
s = rq.Session()
retries = Retry(total=5,
                backoff_factor=1,
                status_forcelist=[ 500, 502, 503, 504 ])
s.mount('http://', HTTPAdapter(max_retries=retries))
distances = []
counter = 0
print("Calculating routes...")
for index, row in routes.iterrows():
  body = '{plan(fromPlace: "::' + str(row['start_lat']) + ',' + str(row['start_lon']) + '", toPlace: "::' + str(row['end_lat']) + ',' + str(row['end_lon']) + '", numItineraries: 1, transportModes: {mode: BICYCLE}) {itineraries{duration legs {distance legGeometry {length points}}}}}'
  request = rq.post(url, data = body, headers = headers)
  if ('data' in request.json()) and (len(request.json()['data']['plan']['itineraries']) > 0): 
    itinerary = request.json()['data']['plan']['itineraries'][0]
    distance = 0
    for leg in itinerary['legs']:
      distance = distance + leg['distance']
    distances.append(distance)
  else:
    distances.append(0)
  counter += 1
  print("Calculated " + str(counter) + " routes")

print(distances)
with open('disstances.csv', 'a') as outfile:
  newFileWriter = csv.writer(outfile) 
  for d in distances:
    newFileWriter.writerow(r)

