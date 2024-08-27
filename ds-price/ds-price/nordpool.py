from .helper import NestedNamespace

resolution = NestedNamespace({
    "HOURLY": 10,
    "DAILY": 11,
    "WEEKLY": 12,
    "MONTHLY": 13,
    "YEARLY": 14,
    })

def resolution_int2str(r):
    if r == resolution.HOURLY: return "Hourly"
    if r == resolution.DAILY: return "Daily"
    if r == resolution.WEEKLY: return "Weekly"
    if r == resolution.MONTHLY: return "Monthly"
    if r == resolution.YEARLY: return "Yearly"


currency = NestedNamespace({
    "EUR": "EUR",
    })

area = NestedNamespace({
    "DE": "DE-LU", # Germany
    "AT": "AT",    # Austria
    "FR": "FR",    # France
    "NL": "NL",    # Netherlands
    "BE": "BE",    # Belgium
    })
