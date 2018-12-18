#!/usr/bin/env python

# Make documentation files for all the Argentina 1902 stations

import pandas
import subprocess

# Get the station metadata (names and locations)
station_names=pandas.read_csv("../../../ToDo/sources/Argentinian_DWR/raw_data/names.csv",
                              skipinitialspace=True,quotechar="'",
                              encoding='utf-8')

# Get the known-bad stations
known_bad=pandas.read_csv("../../../ToDo/sources/Argentinian_DWR/raw_data/known_bad.csv",
                              skipinitialspace=True,quotechar="'",
                              encoding='utf-8')

for id in station_names.SEF_ID.values:
    print(id)
    if id in known_bad.SEF_ID.values:
        proc = subprocess.Popen("./make_docs_one_bad_station.py --id=%s" % id,
                                shell=True)
    else:
        proc = subprocess.Popen("./make_docs_one_station.py --id=%s" % id,
                                shell=True)
    (out, err) = proc.communicate()
