import requests
from datetime import datetime

from . import nordpool as np

def request(resolution, currency, end_date):
    BASE = "https://www.nordpoolgroup.com/api/marketdata/page/{}"
    r = requests.get(
        BASE.format(resolution),
        params={
            "currency": currency,
            "endDate": end_date.strftime("%d-%m-%Y"),
        })
    return r.json()

def parse_response(res, resolution, currency, areas, start_date = None):
    def str2float(s):
        try:
            return float(s.replace(",", "."))
        except ValueError:
            return float("inf")
    result = []
    data = res["data"]
    for r in data["Rows"]:
        row_start_time = datetime.fromisoformat(r["StartTime"])
        if start_date and row_start_time < start_date:
            continue
        row_end_time = datetime.fromisoformat(r["EndTime"])
        if r["IsExtraRow"]:
            continue
        for c in r["Columns"]:
            area = c["Name"]
            if area not in areas:
                continue
            result.append({
                "area": area,
                "start": row_start_time,
                "end": row_end_time,
                "currency": currency,
                "resolution": np.resolution_int2str(resolution),
                "price_per_mwh": str2float(c["Value"])
                })
    return result

def fetch(resolution, currency, areas, end_date, start_date = None):
    res = request(resolution, currency, end_date)
    res = parse_response(res, resolution, currency, areas)
    return res
