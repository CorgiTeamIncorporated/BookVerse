FROM postgres

COPY users.sql /tmp/

COPY 1_schema.sql /docker-entrypoint-initdb.d/
COPY 2_init_permissions.sh /docker-entrypoint-initdb.d/
