from threading import Thread
from queue import SimpleQueue as Queue

from .helper import dt_tomorrow
from . import nordpool as np
from . import api
from . import influxdb

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY
MONTH = 4 * WEEK
YEAR = 12 * MONTH

NUM_WORKERS = 4
THREAD_TIMEOUT_SEC = 10

SENTINEL = None

def worker(id, task_queue, result_queue):
    while True:
        t = task_queue.get()
        if t == SENTINEL:
            print(f"Worker {id} exiting...")
            break
        print(f"Worker {id} receives task: {t}")
        res = api.fetch(t["resolution"], t["currency"], t["areas"], dt_tomorrow())
        result_queue.put(res)

def process(result_queue, cfg, influxdb_client):
    while True:
        res = result_queue.get()
        if res == SENTINEL:
            print("Processor exiting...")
            break
        for r in res:
            p = influxdb.point({
                "measurement": "energy_price",
                "tags": {k: r[k] for k in ["area", "resolution", "currency"]},
                "fields": {k: r[k] for k in ["price_per_mwh"]},
                "time": r["start"]
            })
            influxdb.write_point(influxdb_client,
                                 cfg.influxdb.org,
                                 cfg.influxdb.bucket,
                                 p)

def periodic_enqueue(resolution, tasks, task_queue, exit_event):
    sleep_sec = {np.resolution.HOURLY: HOUR,
                 np.resolution.DAILY: DAY,
                 np.resolution.WEEKLY: WEEK,
                 np.resolution.MONTHLY: MONTH,
                 np.resolution.YEARLY: YEAR}[resolution]
    while not exit_event.is_set():
        for t in tasks:
            task_queue.put(t)
        print("Enqueue task ", t, " and sleep for ", sleep_sec)
        exit_event.wait(sleep_sec)
    print("Periodic enqueue exiting...")

def start(cfg, influxdb_client, exit_event):
    params = cfg.nordpool
    tasks = {}
    for r in params.resolution:
        tasks[r] = [{"resolution": r, "areas": params.areas, "currency": c} for c in params.currency]
    task_queue = Queue()
    result_queue = Queue()
    threads = []
    for r, t in tasks.items():
        th = Thread(target=periodic_enqueue,
                    args=(r, t, task_queue, exit_event))
        threads.append(th)
    for id in range(NUM_WORKERS):
        th = Thread(target=worker,
                    args=(id, task_queue, result_queue))
        threads.append(th)
    th = Thread(target=process, args=(result_queue, cfg, influxdb_client))
    threads.append(th)
    for th in threads:
        th.start()
    while not exit_event.is_set():
        exit_event.wait()
    for _ in range(NUM_WORKERS):
        task_queue.put(SENTINEL)
    result_queue.put(SENTINEL)
    for th in threads:
        th.join(timeout=THREAD_TIMEOUT_SEC)
