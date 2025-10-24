#!/bin/bash

# Case insenstive match
shopt -s nocaseglob

if [ -z "${ENV_FILE}" ]; then
  ENV_FILE="/secrets/env.json"
fi

echo 'Checking for environment file "'${ENV_FILE}'"…'

if [ ! -f "${ENV_FILE}" ]; then
  echo 'Error: Environment file "'${ENV_FILE}'" not found!'
  exit 1
fi

echo 'Using environment file "'${ENV_FILE}'"...'

#echo $DJANGO_SETTINGS_MODULE
#
#if [ -z "${GUNICORN_WORKERS}" ]; then
#    GUNICORN_WORKERS=4
#fi
#
#if [ -z "${GUNICORN_PORT}" ]; then
#    GUNICORN_PORT=5000
#fi
#
#if [ -z "${GUNICORN_TIMEOUT}" ]; then
#    GUNICORN_TIMEOUT=120
#fi
#
#if [ "${GUNICORN_RELOAD}" ]; then
#    GUNICORN_RELOAD="--reload"
#else
#    GUNICORN_RELOAD=""
#fi

#DOMAIN_JQ='.ALLOWED_HOSTS | . - ["127.0.0.1", "localhost", ".ngrok.io"] | if . | length == 0 then "localhost" else .[0] end'
#
#if [ -z "${ENV_JSON}" ]; then
#    MYSQL_HOST=$(jq -r -c ".MYSQL_HOST | values" ${ENV_FILE})
#    MYSQL_PORT=$(jq -r -c ".MYSQL_PORT | values" ${ENV_FILE})
#    IS_CRON_POD=$(jq -r -c ".IS_CRON_POD | values" ${ENV_FILE})
#    PTVSD_ENABLE=$(jq -r -c ".PTVSD_ENABLE | values" ${ENV_FILE})
#    CRONTAB_SCHEDULE=$(jq -r -c ".CRONTAB_SCHEDULE | values" ${ENV_FILE})
#    RUN_AT_TIMES=$(jq -r -c ".RUN_AT_TIMES | values" ${ENV_FILE})
#    DOMAIN=$(jq -r -c "${DOMAIN_JQ} | values" ${ENV_FILE})
#else
#    MYSQL_HOST=$(echo "${ENV_JSON}" | jq -r -c ".MYSQL_HOST | values")
#    MYSQL_PORT=$(echo "${ENV_JSON}" | jq -r -c ".MYSQL_PORT | values")
#    IS_CRON_POD=$(echo "${ENV_JSON}" | jq -r -c ".IS_CRON_POD | values")
#    PTVSD_ENABLE=$(echo "${ENV_JSON}" | jq -r -c ".PTVSD_ENABLE | values")
#    CRONTAB_SCHEDULE=$(echo "${ENV_JSON}" | jq -r -c ".CRONTAB_SCHEDULE | values")
#    RUN_AT_TIMES=$(echo "${ENV_JSON}" | jq -r -c ".RUN_AT_TIMES | values")
#    DOMAIN=$(echo "${ENV_JSON}" | jq -r -c "${DOMAIN_JQ} | values")
#fi

DB_HOST=$(jq -r -c ".DB_HOST | values" ${ENV_FILE})
DB_PORT=$(jq -r -c ".DB_PORT | values" ${ENV_FILE})
DB_TUNNEL_PORT=$(jq -r -c ".DB_TUNNEL_PORT | values" ${ENV_FILE})

echo 'Checking for DB readiness...'
while ! nc -z ${DB_HOST} ${DB_PORT}; do
  echo 'Waiting for DB...'
  sleep 1 # in seconds
done
echo 'DB is ready.'

echo 'Applying Django migrations...'
python manage.py migrate
echo 'Django migrations complete.'

if [ -n "${DB_TUNNEL_PORT}" ]; then
  echo "Opening tunnel on port (${DB_TUNNEL_PORT}) to DB server at (${DB_HOST}:${DB_PORT})..."
  socat "TCP-LISTEN:${DB_TUNNEL_PORT},fork" "TCP:${DB_HOST}:${DB_PORT}" &
fi

echo 'Setting Git info variables…'
export GIT_REPO="$(git config --local remote.origin.url)"
echo "  GIT_REPO=${GIT_REPO}"
export GIT_COMMIT="$(git rev-parse HEAD)"
echo "  GIT_COMMIT=${GIT_COMMIT}"
export GIT_BRANCH="$(git name-rev $GIT_COMMIT --name-only)"
echo "  GIT_BRANCH=${GIT_BRANCH}"

#echo "Setting domain of default site record"
## The value for LOCALHOST_PORT is set in docker-compose.yml
#if [ ${DOMAIN} == "localhost" ]; then
#  python manage.py site --domain="${DOMAIN}:${LOCALHOST_PORT}" --name="${DOMAIN}"
#else
#  python manage.py site --domain="${DOMAIN}" --name="${DOMAIN}"
#fi

echo 'Collecting static files…'
python manage.py collectstatic --noinput

gunicorn KarpeLiber.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120
