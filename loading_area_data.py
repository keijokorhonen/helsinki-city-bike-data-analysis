import os
import numpy as np
import pandas as pnd
import geopandas as gp
import pathlib
import psycopg2
import shapely as shp
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape

engine = create_engine('postgresql+psycopg2:///city_bikes', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

current_folder = pathlib.Path(__file__).parent.absolute()
data_folder = current_folder / "data"

# Load districts from file and write them to table "region" in the database
areas = gp.read_file(data_folder / "Helsinki_osa-alueet.geojson")
espoo = gp.read_file(data_folder / "Espoo_alue.geojson")

class Region(Base):
        __tablename__ = 'region'
        id = Column(Integer, primary_key=True)
        district_id = Column(String)
        municipality = Column(String)
        major_district = Column(String)
        base_district = Column(String)
        sub_district = Column(String)
        name = Column(String)
        geom = Column(Geometry('POLYGON'))
Region.__table__.create(engine)
session = Session()
for index, row in areas.iterrows():
  area = Region(district_id=row['kokotun'], municipality=row['kunta'], major_district=row['suur'], base_district=row['perus'], sub_district=row['osa'], name=row['nimi'], geom=from_shape(row['geometry'], srid=3857))
  session.add(area)
for index, row in espoo.iterrows():
  espoo_area = Region(district_id='0490000000', municipality='049', major_district="0", base_district='000', sub_district='000', name='Espoo', geom=from_shape(row['geometry'], srid=3857))
  session.add(espoo_area)
session.commit()

# Load bike stations from file and write them to the database into table "station" in the database
stations = gp.read_file(data_folder / "kaupunkipyöräasemat.geojson")
class Station(Base):
        __tablename__ = 'station'
        id = Column(Integer, primary_key=True)
        station_id = Column(String)
        name = Column(String)
        address = Column(String)
        city = Column(String)
        operator = Column(String)
        capacity = Column(Integer)
        latitude = Column(Numeric)
        longitude = Column(Numeric)
        geom = Column(Geometry('POINT'))
Station.__table__.create(engine)
session = Session()
for index, row in stations.iterrows():
  station = Station(id=row['FID'], station_id=row['ID'], name=row['Nimi'], address=row['Osoite'], city=row['Kaupunki'], operator=row['Operaattor'], capacity=row['Kapasiteet'], latitude=row['y'], longitude=row['x'],geom=from_shape(row['geometry'], srid=3857))
  session.add(station)
session.commit()

# Create a table for the optimal routes, which can then be linked to individual rides, to be filled later
class Route(Base):
        __tablename__ = 'route'
        id = Column(Integer, primary_key=True)
        start_station_id = Column(String)
        end_station_id = Column(String)
        distance = Column(Numeric)
        duration = Column(Numeric)
        geom = Column(Geometry('LINESTRING'))
        rides = relationship('Ride')
Route.__table__.create(engine)

# Prepare tables for importing rides from raw csv files created by earlier init script
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
Ride.__table__.create(engine)

# Create a temporary table for the raw csv data
class RawRide(Base):
        __tablename__ = 'raw_ride'
        id = Column(Integer, primary_key=True)
        departure_time = Column(DateTime)
        return_time = Column(DateTime)
        departure_station_id = Column(String)
        departure_station_name = Column(String)
        return_station_id = Column(String)
        return_station_name = Column(String)
        distance = Column(Numeric)
        duration = Column(Numeric)
RawRide.__table__.create(engine)

# This takes too long – we'll import the csv sto a temporaty table and do SQL SELECT INTO
# for item in files:
#     for df in pnd.read_csv(f'{current_folder}/data/city-bike-raw/{item}', dtype=str, chunksize=100000, iterator=True):
#       session = Session()
#       df = df.drop(df[df['Departure station id'] == df['Return station id']].index) 
#       df[['Departure Date','Departure Time']] = df['Departure'].str.split('T', 1, expand=True)
#       df['Year'] = df['Departure Date'].str.split('-', 1).str[0]
#       df[['Return Date', 'Return Time']] = df['Return'].str.split('T', 1, expand=True)
#       df = df[['Year', 'Departure', 'Return', 'Departure station id', 'Return station id', 'Covered distance (m)', 'Duration (sec.)']]
#       # df.rename(columns={'Year':'year', 'Departure':'dep_time', 'Return':'ret_time', 'Departure station id':'dep_st_id', 'Return station id':'ret_st_id', 'Covered distance (m)':'distance', 'Duration (sec.)':'duration'})
#       for index, row in df.iterrows():
#         ride = Ride(year=row['Year'], departure_time=row['Departure'], return_time=row['Return'], departure_station_id=row['Departure station id'], return_station_id=row['Return station id'], distance=row['Covered distance (m)'], duration=row['Duration (sec.)']) 
#         session.add(ride)
#       session.commit()


