DO $$
DECLARE
    counter INT := 1;
BEGIN
    WHILE counter <= 5 LOOP
        INSERT INTO actor (actor_name)
        VALUES ('loop actor ' || counter);

        counter := counter + 1;
    END LOOP;
END $$;