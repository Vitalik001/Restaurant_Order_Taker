FROM postgres

WORKDIR /code/db

ENV POSTGRES_PASSWORD=postgres

EXPOSE 5432

ADD create_tables.sql /docker-entrypoint-initdb.d/