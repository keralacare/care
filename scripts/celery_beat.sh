#!/bin/bash
printf "celery-beat" > /tmp/container-role

set -eo pipefail

./wait_for_db.sh
./wait_for_redis.sh

if [[ "${AUTO_MAINTENANCE_MODE}" == "true" ]]; then
    python manage.py maintenance_mode on
fi

python manage.py migrate --noinput
python manage.py compilemessages -v 0
python manage.py load_redis_index

if [[ "${AUTO_MAINTENANCE_MODE}" == "true" ]]; then
    python manage.py maintenance_mode off
fi

touch /tmp/healthy

export NEW_RELIC_CONFIG_FILE=/etc/newrelic.ini
if [[ -f "$NEW_RELIC_CONFIG_FILE" ]]; then
    newrelic-admin run-program celery --app=config.celery_app beat --loglevel=info
else
    celery --app=config.celery_app beat --loglevel=info
fi
