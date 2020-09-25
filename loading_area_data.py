import numpy
import pandas
import geopandas as gp
import pathlib
import sqlalchemy as db

current_folder = pathlib.Path(__file__).parent.absolute();
data_folder = current_folder / "data"

areas = gp.read_file(data_folder / "Helsinki_osa-alueet.geojson");
