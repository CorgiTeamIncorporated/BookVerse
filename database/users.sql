CREATE USER app WITH PASSWORD 'put your password';

--ACCESS DB
REVOKE CONNECT ON DATABASE bookverse FROM PUBLIC;
GRANT  CONNECT ON DATABASE bookverse  TO app;

--ACCESS SCHEMA
REVOKE ALL     ON SCHEMA public FROM PUBLIC;
GRANT  USAGE   ON SCHEMA public  TO app;

--ACCESS TABLES
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
GRANT SELECT, INSERT, UPDATE 
ON ALL TABLES IN SCHEMA public 
TO app;

--ACCESS SEQUENCES
GRANT SELECT, USAGE ON ALL SEQUENCES IN SCHEMA public TO app;

--ACCESS FUTURE TABLES
ALTER DEFAULT PRIVILEGES 
    FOR USER postgres
    IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE ON TABLES TO app;

--ACCESS FUTURE SEQUENCES
ALTER DEFAULT PRIVILEGES 
    FOR USER postgres
    IN SCHEMA public
    GRANT SELECT, USAGE ON SEQUENCES TO app;