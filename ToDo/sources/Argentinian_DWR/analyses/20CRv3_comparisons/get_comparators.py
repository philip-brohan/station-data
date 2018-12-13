#!/usr/bin/env python

# Extract data from 20CRv3 for all the Argentinian stations.

import IRData.twcr as twcr
import iris
import iris.analysis
import pandas
import numpy
import datetime
import pickle
import os
import sys

# Fix dask SPICE bug
import dask
dask.config.set(scheduler='single-threaded')

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", help="year",
                    type=int,required=True)
parser.add_argument("--month", help="month",
                    type=int,required=True)
parser.add_argument("--day", help="day",
                    type=int,required=True)
parser.add_argument("--hour", help="hour",
                    type=int,required=True)
parser.add_argument("--var", help="Variable to extract",
                    type=str,required=True)
parser.add_argument("--opdir", help="Directory for output files",
                    default=("%s/sef_comparators/Argentinian_DWR/" %
                               os.getenv('SCRATCH')),
                    type=str,required=False)

args = parser.parse_args()
args.opdir="%s/%04d/%02d/%02d/%02d" % (args.opdir,args.year,
                                       args.month,args.day,
                                       args.hour)
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir)

# Find the directory with this script in
try:
    bindir=os.path.abspath(os.path.dirname(__file__))
except NameError:
    bindir='.'

# Get the station metadata (names and locations)
station_names=pandas.read_csv("%s/../../raw_data/Positions.csv" % bindir,
                              skipinitialspace=True,quotechar="'",
                              encoding='utf-8')

# Load the 20CRv3 field
rdata=twcr.load(args.var,
                datetime.datetime(args.year,args.month,
                                  args.day,args.hour),
                version='4.5.1')
interpolator = iris.analysis.Linear().interpolator(rdata, 
                                ['latitude', 'longitude'])
 
# Pickle the ensemble at each station
for station in station_names.SEF_ID.values:
   sn=station_names[station_names.SEF_ID==station]
   if numpy.isnan(sn['lat'].values): continue
   ensemble = interpolator([numpy.array(sn['lat'].values[0]),
                            numpy.array(sn['lon'].values[0])]).data
   opfile="%s/%s_%s.pkl" % (args.opdir,station,args.var)
   fh=open(opfile,'wb')
   pickle.dump(ensemble,fh)
   fh.close()
