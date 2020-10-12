import numpy as np
import pandas as pd
import geopandas as gpd
import pathlib
import psycopg2
import geojson
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape
from shapely.geometry import asShape

engine = create_engine('postgresql+psycopg2:///city_bikes', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

current_folder = pathlib.Path(__file__).parent.absolute()
data_folder = current_folder / "data"

# Read ride counts
rides = pd.read_csv(current_folder / "rides_between_districts_full.csv")
rides = rides.drop(columns=["Unnamed: 0"])
rides = rides.astype({"start_district": str, "finish_district": str, "count": int, "day": int}).replace({"start_district": "0", "finish_district": "0"},"000")
# Read base district geometries
helsinki = gpd.read_file(data_folder / "Helsingin_peruspiirit.geojson")
helsinki = helsinki.rename(columns={"asemia": "bike_stations"})
helsinki = helsinki.drop(columns=["kokotunnus", "kunta"])
# Reading Espoo geometry
espoo = gpd.read_file(data_folder / "Espoo_alue.geojson")
espoo["id"] = "000"
espoo = espoo.rename(columns={"KAUPUNKI": "name"})
espoo["name"] = espoo["name"].str.title()
espoo = espoo[["id", "name", "geometry"]]
# Adding Espoo and calculating centroids
espoo = espoo.to_crs(helsinki.crs)
districts = helsinki.append(espoo)
districts = districts.sort_values("id").reset_index(drop=True)
districts["center"] = districts["geometry"].centroid
# Getting demographic data for the districts
dem = pd.read_csv(current_folder / "Demographic_data_new.csv")
dem = dem.drop(columns=["name"])
dem = dem.astype({"id": str})
dem = pd.merge(dem,pd.read_csv(current_folder / "job_types_per_district.csv"), left_index=True, right_index=True)
dem = dem.append(pd.Series({"id": "000"}), ignore_index=True)
dem = dem.sort_values("id").reset_index(drop=True)
dem = pd.merge(dem, districts, on="id")
dem = dem.rename(columns={"id": "base_id"})
dem = dem.replace({np.nan: None})

# Creating the table for base areas
class BaseDistrict(Base):
        __tablename__ = 'base_district'
        id = Column(Integer, primary_key=True)
        base_id = Column(String)
        major_id = Column(Integer)
        total_pop = Column(Integer)
        pop_km2 = Column(Numeric)
        ages_0_6 = Column(Numeric)
        ages_7_15 = Column(Numeric)
        ages_16_18 = Column(Numeric)
        ages_19_24 = Column(Numeric)
        ages_25_39 = Column(Numeric)
        ages_40_64 = Column(Numeric)
        ages_65 = Column(Numeric)
        avg_pers_income = Column(Numeric)
        median_fam_income = Column(Integer)
        people_on_social_assistance = Column(Integer)
        unemployment = Column(Numeric)
        manufacture_jobs = Column(Numeric)
        retail_jobs = Column(Numeric)
        transport_jobs = Column(Numeric)
        business_jobs = Column(Numeric)
        public_jobs = Column(Numeric)
        employment_km2 = Column(Integer)
        homes = Column(Integer)
        business_bldgs = Column(Numeric)
        public_bldgs = Column(Numeric)
        industrial_bldgs = Column(Numeric)
        floorarea_ha = Column(Integer)
        floorarea_housing_house = Column(Numeric)
        floorarea_housing_condo = Column(Numeric)
        floorarea_business = Column(Numeric)
        floorarea_public = Column(Numeric)
        floorarea_industrial = Column(Numeric)
        floorarea_other = Column(Numeric)
        daycares = Column(Integer)
        primary_schools = Column(Integer)
        primary_school_pupils = Column(Integer)
        middle_schools = Column(Integer)
        middle_school_pupils = Column(Integer)
        high_schools = Column(Integer)
        high_school_students = Column(Integer)
        special_schools = Column(Integer)
        special_school_pupils = Column(Integer)
        libraries = Column(Integer)
        health_stations = Column(Integer)
        playgrounds = Column(Integer)
        swimming_halls = Column(Integer)
        sports_halls = Column(Integer)
        sports_fields = Column(Integer)
        churches = Column(Integer)
        post_offices = Column(Integer)
        apothecaries = Column(Integer)
        alkos = Column(Integer)
        grocery_shops = Column(Integer)
        other_retail = Column(Integer)
        restaurants = Column(Integer)
        cafes_bars = Column(Integer)
        parks_ha = Column(Numeric)
        forest_ha = Column(Numeric)
        swim_beaches = Column(Integer)
        voted_SDP = Column(Numeric)
        voted_KOK = Column(Numeric)
        voted_VIHR = Column(Numeric)
        voted_RKP = Column(Numeric)
        voted_VASL = Column(Numeric)
        voted_PS = Column(Numeric)
        voted_other = Column(Numeric)
        geometry = Column(Geometry('POLYGON'))
        center = Column(Geometry('POINT'))
        bike_stations = Column(Integer)
        rides_in_sun_morning = Column(Integer)
        rides_in_sun_day = Column(Integer)
        rides_in_sun_evening = Column(Integer)
        rides_in_sun_night = Column(Integer)
        rides_in_mon_morning = Column(Integer)
        rides_in_mon_day = Column(Integer)
        rides_in_mon_evening = Column(Integer)
        rides_in_mon_night = Column(Integer)
        rides_in_tue_morning = Column(Integer)
        rides_in_tue_day = Column(Integer)
        rides_in_tue_evening = Column(Integer)
        rides_in_tue_night = Column(Integer)
        rides_in_wed_morning = Column(Integer)
        rides_in_wed_day = Column(Integer)
        rides_in_wed_evening = Column(Integer)
        rides_in_wed_night = Column(Integer)
        rides_in_thu_morning = Column(Integer)
        rides_in_thu_day = Column(Integer)
        rides_in_thu_evening = Column(Integer)
        rides_in_thu_night = Column(Integer)
        rides_in_fri_morning = Column(Integer)
        rides_in_fri_day = Column(Integer)
        rides_in_fri_evening = Column(Integer)
        rides_in_fri_night = Column(Integer)
        rides_in_sat_morning = Column(Integer)
        rides_in_sat_day = Column(Integer)
        rides_in_sat_evening = Column(Integer)
        rides_in_sat_night = Column(Integer)
        rides_out_sun_morning = Column(Integer)
        rides_out_sun_day = Column(Integer)
        rides_out_sun_evening = Column(Integer)
        rides_out_sun_night = Column(Integer)
        rides_out_mon_morning = Column(Integer)
        rides_out_mon_day = Column(Integer)
        rides_out_mon_evening = Column(Integer)
        rides_out_mon_night = Column(Integer)
        rides_out_tue_morning = Column(Integer)
        rides_out_tue_day = Column(Integer)
        rides_out_tue_evening = Column(Integer)
        rides_out_tue_night = Column(Integer)
        rides_out_wed_morning = Column(Integer)
        rides_out_wed_day = Column(Integer)
        rides_out_wed_evening = Column(Integer)
        rides_out_wed_night = Column(Integer)
        rides_out_thu_morning = Column(Integer)
        rides_out_thu_day = Column(Integer)
        rides_out_thu_evening = Column(Integer)
        rides_out_thu_night = Column(Integer)
        rides_out_fri_morning = Column(Integer)
        rides_out_fri_day = Column(Integer)
        rides_out_fri_evening = Column(Integer)
        rides_out_fri_night = Column(Integer)
        rides_out_sat_morning = Column(Integer)
        rides_out_sat_day = Column(Integer)
        rides_out_sat_evening = Column(Integer)
        rides_out_sat_night = Column(Integer)
        rides_within_sun_morning = Column(Integer)
        rides_within_sun_day = Column(Integer)
        rides_within_sun_evening = Column(Integer)
        rides_within_sun_night = Column(Integer)
        rides_within_mon_morning = Column(Integer)
        rides_within_mon_day = Column(Integer)
        rides_within_mon_evening = Column(Integer)
        rides_within_mon_night = Column(Integer)
        rides_within_tue_morning = Column(Integer)
        rides_within_tue_day = Column(Integer)
        rides_within_tue_evening = Column(Integer)
        rides_within_tue_night = Column(Integer)
        rides_within_wed_morning = Column(Integer)
        rides_within_wed_day = Column(Integer)
        rides_within_wed_evening = Column(Integer)
        rides_within_wed_night = Column(Integer)
        rides_within_thu_morning = Column(Integer)
        rides_within_thu_day = Column(Integer)
        rides_within_thu_evening = Column(Integer)
        rides_within_thu_night = Column(Integer)
        rides_within_fri_morning = Column(Integer)
        rides_within_fri_day = Column(Integer)
        rides_within_fri_evening = Column(Integer)
        rides_within_fri_night = Column(Integer)
        rides_within_sat_morning = Column(Integer)
        rides_within_sat_day = Column(Integer)
        rides_within_sat_evening = Column(Integer)
        rides_within_sat_night = Column(Integer)
BaseDistrict.__table__.create(engine)

session = Session()
for index, row in dem.iterrows():
  base_district = BaseDistrict(
        base_id = row['base_id'],
        major_id = row['major_id'],
        total_pop = row['total_pop'],
        pop_km2 = row['pop_km2'],
        ages_0_6 = row['ages_0-6'],
        ages_7_15 = row['ages_7-15'],
        ages_16_18 = row['ages_16-18'],
        ages_19_24 = row['ages_19-24'],
        ages_25_39 = row['ages_25-39'],
        ages_40_64 = row['ages_40-64'],
        ages_65 = row['ages_65-'],
        avg_pers_income = row['avg_pers_income'],
        median_fam_income = row['median_fam_income'],
        people_on_social_assistance = row['people_on_social_assistance'],
        unemployment = row['unemployment'],
        manufacture_jobs = row['manufacture_jobs'],
        retail_jobs = row['retail_jobs'],
        transport_jobs = row['transport_jobs'],
        business_jobs = row['business_jobs'],
        public_jobs = row['public_jobs'],
        employment_km2 = row['employment_km2'],
        homes = row['homes'],
        business_bldgs = row['business_bldgs'],
        public_bldgs = row['public_bldgs'],
        industrial_bldgs = row['industrial_bldgs'],
        floorarea_ha = row['floorarea_ha'],
        floorarea_housing_house = row['floorarea_housing_house'],
        floorarea_housing_condo = row['floorarea_housing_condo'],
        floorarea_business = row['floorarea_business'],
        floorarea_public = row['floorarea_public'],
        floorarea_industrial = row['floorarea_industrial'],
        floorarea_other = row['floorarea_other'],
        daycares = row['daycares'],
        primary_schools = row['primary_schools'],
        primary_school_pupils = row['primary_school_pupils'],
        middle_schools = row['middle_schools'],
        middle_school_pupils = row['middle_school_pupils'],
        high_schools = row['high_schools'],
        high_school_students = row['high_school_students'],
        special_schools = row['special_schools'],
        special_school_pupils = row['special_school_pupils'],
        libraries = row['libraries'],
        health_stations = row['health_stations'],
        playgrounds = row['playgrounds'],
        swimming_halls = row['swimming_halls'],
        sports_halls = row['sports_halls'],
        sports_fields = row['sports_fields'],
        churches = row['churches'],
        post_offices = row['post_offices'],
        apothecaries = row['apothecaries'],
        alkos = row['alkos'],
        grocery_shops = row['grocery_shops'],
        other_retail = row['other_retail'],
        restaurants = row['restaurants'],
        cafes_bars = row['cafes_bars'],
        parks_ha = row['parks_ha'],
        forest_ha = row['forest_ha'],
        swim_beaches = row['swim_beaches'],
        voted_SDP = row['voted_SDP'],
        voted_KOK = row['voted_KOK'],
        voted_VIHR = row['voted_VIHR'],
        voted_RKP = row['voted_RKP'],
        voted_VASL = row['voted_VASL'],
        voted_PS = row['voted_PS'],
        voted_other = row['voted_other'],
       geometry = asShape(row['geometry']).wkb_hex,
       center = asShape(row['center']).wkb_hex,
       bike_stations = row['bike_stations'],
        rides_in_sun_morning = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 0) & (rides['time'] == 'morning')]['count'].sum()),
        rides_in_sun_day = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 0) & (rides['time'] == 'day')]['count'].sum()),
        rides_in_sun_evening = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 0) & (rides['time'] == 'evening')]['count'].sum()),
        rides_in_sun_night = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 0) & (rides['time'] == 'night')]['count'].sum()),
        rides_in_mon_morning = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 1) & (rides['time'] == 'morning')]['count'].sum()),
        rides_in_mon_day = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 1) & (rides['time'] == 'day')]['count'].sum()),
        rides_in_mon_evening = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 1) & (rides['time'] == 'evening')]['count'].sum()),
        rides_in_mon_night = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 1) & (rides['time'] == 'night')]['count'].sum()),
        rides_in_tue_morning = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 2) & (rides['time'] == 'morning')]['count'].sum()),
        rides_in_tue_day = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 2) & (rides['time'] == 'day')]['count'].sum()),
        rides_in_tue_evening = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 2) & (rides['time'] == 'evening')]['count'].sum()),
        rides_in_tue_night = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 2) & (rides['time'] == 'night')]['count'].sum()),
        rides_in_wed_morning = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 3) & (rides['time'] == 'morning')]['count'].sum()),
        rides_in_wed_day = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 3) & (rides['time'] == 'day')]['count'].sum()),
        rides_in_wed_evening = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 3) & (rides['time'] == 'evening')]['count'].sum()),
        rides_in_wed_night = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 3) & (rides['time'] == 'night')]['count'].sum()),
        rides_in_thu_morning = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 4) & (rides['time'] == 'morning')]['count'].sum()),
        rides_in_thu_day = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 4) & (rides['time'] == 'day')]['count'].sum()),
        rides_in_thu_evening = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 4) & (rides['time'] == 'evening')]['count'].sum()),
        rides_in_thu_night = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 4) & (rides['time'] == 'night')]['count'].sum()),
        rides_in_fri_morning = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 5) & (rides['time'] == 'morning')]['count'].sum()),
        rides_in_fri_day = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 5) & (rides['time'] == 'day')]['count'].sum()),
        rides_in_fri_evening = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 5) & (rides['time'] == 'evening')]['count'].sum()),
        rides_in_fri_night = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 5) & (rides['time'] == 'night')]['count'].sum()),
        rides_in_sat_morning = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 6) & (rides['time'] == 'morning')]['count'].sum()),
        rides_in_sat_day = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 6) & (rides['time'] == 'day')]['count'].sum()),
        rides_in_sat_evening = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 6) & (rides['time'] == 'evening')]['count'].sum()),
        rides_in_sat_night = int(rides.loc[(rides['start_district'] != row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 6) & (rides['time'] == 'night')]['count'].sum()),
        rides_out_sun_morning = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 0) & (rides['time'] == 'morning')]['count'].sum()),
        rides_out_sun_day = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 0) & (rides['time'] == 'day')]['count'].sum()),
        rides_out_sun_evening = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 0) & (rides['time'] == 'evening')]['count'].sum()),
        rides_out_sun_night = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 0) & (rides['time'] == 'night')]['count'].sum()),
        rides_out_mon_morning = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 1) & (rides['time'] == 'morning')]['count'].sum()),
        rides_out_mon_day = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 1) & (rides['time'] == 'day')]['count'].sum()),
        rides_out_mon_evening = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 1) & (rides['time'] == 'evening')]['count'].sum()),
        rides_out_mon_night = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 1) & (rides['time'] == 'night')]['count'].sum()),
        rides_out_tue_morning = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 2) & (rides['time'] == 'morning')]['count'].sum()),
        rides_out_tue_day = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 2) & (rides['time'] == 'day')]['count'].sum()),
        rides_out_tue_evening = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 2) & (rides['time'] == 'evening')]['count'].sum()),
        rides_out_tue_night = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 2) & (rides['time'] == 'night')]['count'].sum()),
        rides_out_wed_morning = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 3) & (rides['time'] == 'morning')]['count'].sum()),
        rides_out_wed_day = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 3) & (rides['time'] == 'day')]['count'].sum()),
        rides_out_wed_evening = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 3) & (rides['time'] == 'evening')]['count'].sum()),
        rides_out_wed_night = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 3) & (rides['time'] == 'night')]['count'].sum()),
        rides_out_thu_morning = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 4) & (rides['time'] == 'morning')]['count'].sum()),
        rides_out_thu_day = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 4) & (rides['time'] == 'day')]['count'].sum()),
        rides_out_thu_evening = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 4) & (rides['time'] == 'evening')]['count'].sum()),
        rides_out_thu_night = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 4) & (rides['time'] == 'night')]['count'].sum()),
        rides_out_fri_morning = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 5) & (rides['time'] == 'morning')]['count'].sum()),
        rides_out_fri_day = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 5) & (rides['time'] == 'day')]['count'].sum()),
        rides_out_fri_evening = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 5) & (rides['time'] == 'evening')]['count'].sum()),
        rides_out_fri_night = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 5) & (rides['time'] == 'night')]['count'].sum()),
        rides_out_sat_morning = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 6) & (rides['time'] == 'morning')]['count'].sum()),
        rides_out_sat_day = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 6) & (rides['time'] == 'day')]['count'].sum()),
        rides_out_sat_evening = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 6) & (rides['time'] == 'evening')]['count'].sum()),
        rides_out_sat_night = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] != row['base_id']) & (rides['day'] == 6) & (rides['time'] == 'night')]['count'].sum()),
        rides_within_sun_morning = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 0) & (rides['time'] == 'morning')]['count'].sum()),
        rides_within_sun_day = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 0) & (rides['time'] == 'day')]['count'].sum()),
        rides_within_sun_evening = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 0) & (rides['time'] == 'evening')]['count'].sum()),
        rides_within_sun_night = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 0) & (rides['time'] == 'night')]['count'].sum()),
        rides_within_mon_morning = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 1) & (rides['time'] == 'morning')]['count'].sum()),
        rides_within_mon_day = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 1) & (rides['time'] == 'day')]['count'].sum()),
        rides_within_mon_evening = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 1) & (rides['time'] == 'evening')]['count'].sum()),
        rides_within_mon_night = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 1) & (rides['time'] == 'night')]['count'].sum()),
        rides_within_tue_morning = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 2) & (rides['time'] == 'morning')]['count'].sum()),
        rides_within_tue_day = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 2) & (rides['time'] == 'day')]['count'].sum()),
        rides_within_tue_evening = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 2) & (rides['time'] == 'evening')]['count'].sum()),
        rides_within_tue_night = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 2) & (rides['time'] == 'night')]['count'].sum()),
        rides_within_wed_morning = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 3) & (rides['time'] == 'morning')]['count'].sum()),
        rides_within_wed_day = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 3) & (rides['time'] == 'day')]['count'].sum()),
        rides_within_wed_evening = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 3) & (rides['time'] == 'evening')]['count'].sum()),
        rides_within_wed_night = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 3) & (rides['time'] == 'night')]['count'].sum()),
        rides_within_thu_morning = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 4) & (rides['time'] == 'morning')]['count'].sum()),
        rides_within_thu_day = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 4) & (rides['time'] == 'day')]['count'].sum()),
        rides_within_thu_evening = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 4) & (rides['time'] == 'evening')]['count'].sum()),
        rides_within_thu_night = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 4) & (rides['time'] == 'night')]['count'].sum()),
        rides_within_fri_morning = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 5) & (rides['time'] == 'morning')]['count'].sum()),
        rides_within_fri_day = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 5) & (rides['time'] == 'day')]['count'].sum()),
        rides_within_fri_evening = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 5) & (rides['time'] == 'evening')]['count'].sum()),
        rides_within_fri_night = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 5) & (rides['time'] == 'night')]['count'].sum()),
        rides_within_sat_morning = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 6) & (rides['time'] == 'morning')]['count'].sum()),
        rides_within_sat_day = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 6) & (rides['time'] == 'day')]['count'].sum()),
        rides_within_sat_evening = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 6) & (rides['time'] == 'evening')]['count'].sum()),
        rides_within_sat_night = int(rides.loc[(rides['start_district'] == row['base_id']) & (rides['finish_district'] == row['base_id']) & (rides['day'] == 6) & (rides['time'] == 'night')]['count'].sum()))
  session.add(base_district)
session.commit()  
engine.dispose()