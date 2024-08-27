from influxdb_client import InfluxDBClient
from influxdb_client.client.write.point import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time

PING_WAIT_SEC = 2

def new(url, token, org):
    c = InfluxDBClient(url, token, org)
    while not c.ping():
        print("Pinging influxdb...")
        time.sleep(PING_WAIT_SEC)
    return c

def point(d):
    return Point.from_dict(d)

def write_point(client, org, bucket, point):
    with client.write_api(write_options=SYNCHRONOUS) as w:
        w.write(bucket=bucket, org=org, record=point)
