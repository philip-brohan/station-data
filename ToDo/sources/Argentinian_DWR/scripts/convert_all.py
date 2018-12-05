#!/usr/bin/env python

# Make CIF files for all the Argentina 1902 stations

import os
import pandas
import subprocess

# Find the directory with this script in
try:
    bindir=os.path.abspath(os.path.dirname(__file__))
except NameError:
    bindir='.'

# Get the station metadata (names and locations)
station_names=pandas.read_csv("%s/../raw_data/names.csv" % bindir,
                              skipinitialspace=True,quotechar="'",
                              encoding='utf-8')

for id in station_names.CIF_ID.values:
    print(id)
    proc = subprocess.Popen("%s/convert_station.py --id=%s" % (bindir,id),
                            shell=True)
    (out, err) = proc.communicate()
