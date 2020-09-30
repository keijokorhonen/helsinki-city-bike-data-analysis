ALTER TABLE station ADD region_id INT;
ALTER TABLE station ADD FOREIGN KEY(district_id) REFERENCES district(id) ON DELETE SET NULL;

CREATE OR REPLACE PROCEDURE public.add_districts_to_stations(
	)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
  counter INTEGER := 0;
BEGIN
LOOP
    UPDATE station AS s SET district_id = counter WHERE ST_Within(s.geom, (SELECT geom FROM district WHERE id = counter)); 
    counter := counter + 1;
    IF counter > (SELECT MAX(id) FROM district) THEN
        EXIT;
    END IF;
END LOOP;
END;
$BODY$;

COMMENT ON PROCEDURE public.add_districts_to_stations()
    IS 'Calculates and adds references to the district in which the station is located.';

