#!/usr/bin/env python

# Plot comparators for all the Argentina 1902 stations

import os
import pandas

# Get the station metadata (names and locations)
station_names=pandas.read_csv("../../raw_data/names.csv",
                              skipinitialspace=True,quotechar="'",
                              encoding='utf-8')
f=open("run.txt","w+")
for id in station_names.SEF_ID.values:
    f.write("./plot_pressure_comparison.py --id=%s\n" % id)
    f.write("./plot_T_comparison.py --id=%s\n" % id)
    #f.write("./highlighted_station_map.py --id=%s\n" % id)
f.close()
