from datetime import datetime
import config

def filter_latitude(record):
    return  config.MIN_LATITUDE <= record.get("Latitude", 0) <= config.MAX_LATITUDE

def filter_longitude(record):
    return config.MIN_LONGITUDE <= record.get("Longitude", 0) <= config.MAX_LONGITUDE

def filter_accuracy(record):
    return config.MIN_ACCURACY <= record.get("Accuracy", 0) <= config.MAX_ACCURACY

def filter_threatstatus(record):
    return record.get("ThreatStatus", "Unknown") != config.IGNORE_THREAT_STATUS

MIN_OBSERVED_DATE_DT = datetime.strptime(config.MIN_OBSERVED_DATE, "%Y-%m-%d")

def filter_date(record):
    try:
        observed_date = datetime.strptime(record["DateObserved"], "%Y-%m-%d")
        return observed_date > MIN_OBSERVED_DATE_DT
    except (KeyError, ValueError):
        return False