import diskcache as dc
import time
from datetime import datetime

cache_dir = dc.Cache('./cache_dir')

def remainingTime():
    currentTime = time.ctime()
    return currentTime

def setCache(key, value, dayTimeout=1, hourTimeout = 24):
    cache_dir.set(key=key, value=value, expire=dayTimeout * hourTimeout * 60 * 60)

def getCachedData(key):
    return cache_dir.get(key=key)