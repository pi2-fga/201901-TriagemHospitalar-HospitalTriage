#!/bin/bash

psql -U postgres -c "CREATE DATABASE myproject;"
psql -U postgres -c "CREATE USER myprojectuser WITH PASSWORD 'password';"
psql -U postgres -c "ALTER ROLE myprojectuser SET client_encoding TO 'utf8';"
psql -U postgres -c "ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';"
psql -U postgres -c "ALTER ROLE myprojectuser SET timezone TO 'UTC';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;"
