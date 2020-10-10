import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2:///city_bikes', echo=True)

query = """SELECT d.start_district, d.finish_district, SUM(d.count) AS count, SUM(d.total_distance) AS total_distance, SUM(d.total_duration) AS total_duration, d.dow AS day, d.time AS time
FROM (SELECT t.route_id, t.c AS count, t.c*t.distance AS total_distance, t.c*t.duration AS total_duration, t.start_district, t.finish_district, t.dow, t.time 
    FROM (SELECT route_id, Count(ride.route_id) AS c, route.distance, route.duration, route.start_base_district AS start_district, route.finish_base_district AS finish_district,
    DATE_PART('dow', departure_time) AS dow,
    CASE WHEN DATE_PART('hour', departure_time) >= 0 AND DATE_PART('hour', departure_time) < 6 THEN 'night' 
    WHEN DATE_PART('hour', departure_time) >= 6 AND DATE_PART('hour', departure_time) < 12 THEN 'morning'
    WHEN DATE_PART('hour', departure_time) >= 12 AND DATE_PART('hour', departure_time) < 18 THEN 'day'
    WHEN DATE_PART('hour', departure_time) >= 18 AND DATE_PART('hour', departure_time) < 24 THEN 'evening' END AS time  
        FROM ride 
        LEFT JOIN route ON route.id = ride.route_id 
        GROUP BY ride.route_id, route.distance, route.duration, route.start_base_district, route.finish_base_district, departure_time
        ) AS t
    ) AS d
    GROUP BY d.start_district, d.finish_district, d.dow, d.time;
"""
df = pd.read_sql(query, engine)
df = df.dropna()
df.to_csv("rides_between_districts_by_time.csv")
engine.dispose()
