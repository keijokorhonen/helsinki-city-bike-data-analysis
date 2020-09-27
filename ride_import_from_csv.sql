
COPY raw_ride (departure_time, return_time, departure_station_id, departure_station_name, return_station_id, return_station_name, distance, duration) 
  FROM '/home/vmarttil/Desktop/2019.csv'
  WITH (format csv, header);

INSERT INTO ride
SELECT id, departure_time, return_time, departure_station_id, return_station_id, distance, duration
  FROM raw_ride
  WHERE (CAST(departure_station_id AS Integer) < 500 OR CAST(return_station_id AS Integer) < 500) 
    AND (departure_station_id != return_station_id OR (distance >= 100 AND duration >= 120));
