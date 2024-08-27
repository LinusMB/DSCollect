#!/bin/sh

# The telegraf bucket is created automatically by influxdb as the initial bucket during the setup step, which is triggered
# when InfluxDB finds that no data has been written yet
# (in the logs influxdb mentions a boltdb file. boltdb is the storage engine used)
# and all the env variables DOCKER_INFLUXDB_INIT_* are present.
# Therefore we are updating instead or creating a new bucket.
# Unfortunately there doesn't seem to be a way not to provide an initial bucket. InfluxDB fails if DOCKER_INFLUXDB_INIT_BUCKET is not set.
# I think it would be better to create all buckets using these scripts since it is more consistent with all the setup located in one place.

set -xue

bucket_description="System metrics"

influx bucket update \
    --id "$DOCKER_INFLUXDB_INIT_BUCKET_ID" \
    --description "$bucket_description" \
