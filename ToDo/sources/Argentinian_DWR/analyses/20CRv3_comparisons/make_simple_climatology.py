#!/usr/bin/env python

# Make a 20CRv3 climatology over a short period

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
parser.add_argument("--hour", help="hour: 0,3,6,9,12,15,18, or 21",
                    type=int,required=True)
parser.add_argument("--var", help="Variable: prmsl, air.2m, ...",
                    type=str,required=True)
parser.add_argument("--version", help="Versoion: 4.5.1, 4.6.1",
                    type=str,required=True)

args = parser.parse_args()

start=datetime.datetime(1902,8,1,0)+datetime.timedelta(hours=args.hour)
end=datetime.datetime(1902,8,31,23,59)
opdir="%s/simple_climatologies/20CRv3/August_1902" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Make the field average over the time
accum=None
current=start
count=0
while current<end:
    rdata=twcr.load(args.var,current,level=925,version=args.version)
    rdata=rdata.collapsed('member', iris.analysis.MEAN)
    if accum is None:
        accum=rdata
    else:
        accum.data=accum.data+rdata.data
    count=count+1
    current=current+datetime.timedelta(days=1)

# pickle the field mean
accum.data=accum.data/count
opfile="%s/%s_925_%s.pkl" % (opdir,args.var,args.version)
fh=open(opfile,'wb')
pickle.dump(accum,fh)
fh.close()
