from os import path, getcwd
from threading import Event
import signal

from . import config
from . import influxdb
from . import periodicservice

CONFIG_FILE_PATH = path.join(getcwd(), "config.json")

def init_exit_event():
    exit_event = Event()
    def handle(signo, _):
        print(f"Received signal {signo}, shutting down...")
        exit_event.set()
    signal.signal(signal.SIGTERM, handle)
    return exit_event

def main():
    cfg = config.new(CONFIG_FILE_PATH)
    exit_event = init_exit_event()
    with influxdb.new(cfg.influxdb.url,
                      cfg.influxdb.token,
                      cfg.influxdb.org) as client:
        periodicservice.start(cfg, client, exit_event)

if __name__ == "__main__":
    main()
