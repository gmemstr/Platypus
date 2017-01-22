# Updated cache script based on mcadmin.
# Includes timelog toggle so dates are not
# logged at all.
import json
import time


def Stash(data, filename, timelog=True):
    today = time.strftime("%x")

    with open("src/cache/" + filename + ".json") as cache:
        _cache = json.load(cache)

    if timelog:
        _cache[today] = data
    else:
        _cache = data

    with open("src/cache/" + filename + ".json", "w") as cache:
        json.dump(_cache, cache, indent=4)


def Fetch(filename, timelog=True, range="today"):
    today = time.strftime("%x")

    with open("src/cache/" + filename + ".json") as cache:
        _data = json.load(cache)

    if timelog:
        if range == "today":
            return _data[today]
        if range == "all":
            return _data
        else:
            return _data[range]
    else:
        return _data
