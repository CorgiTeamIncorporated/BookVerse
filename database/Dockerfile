FROM postgres

ENV POSTGRES_DB=bookverse
ENV POSTGRES_PASSWORD=put_your_password

COPY schema.sql /docker-entrypoint-initdb.d/
COPY users.sql /docker-entrypoint-initdb.d/
