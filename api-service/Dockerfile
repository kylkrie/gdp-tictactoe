#####################
# Local development stage
# dev mode, hot reloading
#####################
FROM python:3.9.19 AS local
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# use layer caching to keep build times as low as possible
# install packages first, then copy src after

# copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy src
COPY ./migrations ./migrations
COPY ./app ./app
COPY ./run_migrations.py .

EXPOSE 4000

# local dev start script
COPY ./start_local.sh .
RUN chmod +x start_local.sh
CMD ["./start_local.sh"]

#####################
# Production stage
# python isn't compiled so I didn't see the need for a builder stage
# if there were C extensions, or the need to compile numpy/pandas for example
# then it could be beneficial to have a builder stage to do that step
# the idea is to keep the production image small by keeping
# build-time dependencies out of the production image
#####################

# alpine is a smaller base image for production
# use specific image tag for reproducibility
FROM python:3.9.19-alpine AS production

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# use layer caching to keep build times as low as possible
# install packages first, then copy src after

# copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy src
COPY ./migrations ./migrations
COPY ./app ./app
COPY ./tests ./tests
COPY ./pytest.ini .
COPY ./run_migrations.py .
COPY ./start_prod.sh .

# create non-root user
RUN adduser -D api
# change owner of app dir
RUN chown -R api:api /usr/src/app
USER api

# run start script
RUN chmod +x ./start_prod.sh
CMD ["./start_prod.sh"]
