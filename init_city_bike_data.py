import wget
import zipfile
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
years = ['2016', '2017', '2019']

if not os.path.exists(f'{dir_path}/data/city-bike-raw/'):
    os.makedirs(f'{dir_path}/data/city-bike-raw/')

for year in years:
    url = f'https://dev.hsl.fi/citybikes/od-trips-{year}/od-trips-{year}.zip'
    filename = wget.download(url, f'{dir_path}/data/')
    with zipfile.ZipFile(filename,'r') as zip_ref:
        zip_ref.extractall(f'{dir_path}/data/city-bike-raw/')
    os.remove(filename)

    if year == '2019':
        for item in os.listdir(f'{dir_path}/data/city-bike-raw/od-trips-2019'):
            os.rename(f'{dir_path}/data/city-bike-raw/od-trips-2019/{item}', f'{dir_path}/data/city-bike-raw/{item}')
        os.rmdir(f'{dir_path}/data/city-bike-raw/od-trips-2019')

import pandas as pd
import sqlalchemy as db

if os.path.exists(f'{dir_path}/city_bikes.db'):
    os.remove(f'{dir_path}/city_bikes.db')

database = db.create_engine(f'sqlite:///{dir_path}/city_bikes.db')
# database = db.create_engine(f'postgresql://user:pass@localhost/city_bikes')

for item in [f for f in os.listdir(f'{dir_path}/data/city-bike-raw/') if f.startswith(tuple(years))]:
    for df in pd.read_csv(f'{dir_path}/data/city-bike-raw/{item}', chunksize=100000, iterator=True):
        df = df.drop(df[df['Departure station id'] == df['Return station id']].index) 

        df[['Departure Date','Departure Time']] = df['Departure'].str.split('T', 1, expand=True)
        df['Year'] = df['Departure Date'].str.split('-', 1).str[0]

        df[['Return Date', 'Return Time']] = df['Return'].str.split('T', 1, expand=True)

        df = df[['Year', 'Departure Date', 'Departure Time', 'Return Date', 'Return Time', 'Departure station id', 'Departure station name', 'Return station id', 'Return station name', 'Covered distance (m)', 'Duration (sec.)']]
        
        df.rename(columns={'Year':'year', 'Departure Date':'dep_date', 'Departure Time':'dep_time', 'Return Date':'ret_date', 'Return Time':'ret_time', 'Departure station id':'dep_st_id', 'Departure station name':'dep_st_name', 'Return station id':'ret_st_id', 'Return station name':'ret_st_name', 'Covered distance (m)':'distance', 'Duration (sec.)':'duration'})

        df.to_sql('city_bikes', database, if_exists='append', index=False)