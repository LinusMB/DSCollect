import json
import os

from .helper import NestedNamespace

def new(file_path):
    with open(file_path) as f:
        d = json.load(f)
    d["influxdb"].setdefault("token",
                             os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"))
    d["influxdb"].setdefault("org",
                             os.environ.get("DOCKER_INFLUXDB_INIT_ORG"))
    d["influxdb"].setdefault("bucket",
                             os.environ.get("DSCOLLECT_BUCKET_NAME"))
    return NestedNamespace(d)
