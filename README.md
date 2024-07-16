# Fix the News - a news comparison website

This is the backend for the Fix the News app. An app that
allows users to upload news content to compare, like and 
comment upon. A scoring system is used to dictate which news
items appear in a user's feed.

## docker-compose
This project uses docker compose locally. To start the project
run:
>docker-compose up

## Makefile
This project uses Make files for running command commands such
as database migrations. To view all commands run:
>make

## Test data
To load data for use in development run:
> make manage ARGS="create_development_data"
