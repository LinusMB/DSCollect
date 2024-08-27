#!/bin/sh

set -xue

bucket_name="price"
bucket_description="Energy price data"
bucket_retention="0"

influx bucket create \
    --org-id "$DOCKER_INFLUXDB_INIT_ORG_ID" \
    --name "$bucket_name" \
    --description "$bucket_description" \
    --retention "$bucket_retention"
