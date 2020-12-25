#!/bin/bash

psql -d $POSTGRES_DB --set "APP_USER=$APP_USER" \
                     --set "APP_PASSWORD=$APP_PASSWORD" \
                     --set "POSTGRES_DB=$POSTGRES_DB" \
                     -c "\i /tmp/users.sql"
