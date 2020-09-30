ALTER TABLE public.route ADD COLUMN start_district integer;
ALTER TABLE public.route ADD COLUMN through_districts integer[];
ALTER TABLE public.route ADD COLUMN finish_district integer;

ALTER TABLE public.route ADD FOREIGN KEY(start_district) REFERENCES district(id) ON DELETE SET NULL;
ALTER TABLE public.route ADD FOREIGN KEY(through_districts) REFERENCES district(id) ON DELETE SET NULL;
ALTER TABLE public.route ADD FOREIGN KEY(finish_district) REFERENCES district(id) ON DELETE SET NULL;

ALTER TABLE public.station ADD UNIQUE (station_id);
	
ALTER TABLE public.ride ADD FOREIGN KEY(departure_station_id) REFERENCES station(station_id) ON DELETE SET NULL;
ALTER TABLE public.ride ADD FOREIGN KEY(return_station_id) REFERENCES station(station_id) ON DELETE SET NULL;


