# Kulumasiina

## Project setup:
- Postgres server external to this repo. Server has a dedicated DB and user for 
  this project
- API as a docker container, python w/ flask & sqlalchemy
- Frontend written with svelte, built to static files and served by a NGINX
  container. Container also routes traffic to api.
