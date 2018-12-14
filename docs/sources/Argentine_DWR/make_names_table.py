#!/usr/bin/env python

# Make an rst table containing links to the station page for each station

import pandas

# Get the station names
station_names=pandas.read_csv("../../../../ToDo/sources/Argentinian_DWR/raw_data/names.csv",
                              skipinitialspace=True,quotechar="'",
                              encoding='utf-8')

print ".. list-table:: "
print "   :widths: 50 50 50"
print "   :header-rows: 0"

i=0
for id in station_names.SEF_ID.values:
    if i%3==0:
        print "   * - %s" % id
    else:
        print "     - %s" % id
    i=i+1

