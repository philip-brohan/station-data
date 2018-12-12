#!/usr/bin/env python

# Make a SEF files from the DWR data

import os
import pandas
import DWR
import SEF
import datetime

# Find the directory with this script in
try:
    bindir=os.path.abspath(os.path.dirname(__file__))
except NameError:
    bindir='.'

# Get the DWR data for 1902
obs=DWR.load_observations('prmsl',
                          datetime.datetime(1902,1,1,0),
                          datetime.datetime(1902,12,31,23))
# Where to put the output files
opdir="%s/../../../sef/UK_DWR/1902" % bindir
if not os.path.isdir(opdir):
    os.makedirs(opdir)

stations=list(set(obs['name']))
for station in stations:
   obs_s=obs[obs['name']==station]
   ob_hhmm=["%2d%02d" % (obs_s['hour'].values[i],
                         obs_s['minute'].values[i]) for i in range(len(obs_s))]
   sef=SEF.create(version='0.0.1')
   sef['ID']=station
   sef['Name']=DWR.pretty_name(station)
   sef['Lat']=obs['latitude'].values[0]
   sef['Lon']=obs['longitude'].values[0]
   sef['Alt']=None
   sef['Source']=None
   sef['Repo']=None
   sef['Var']='msl pressure'
   sef['Units']='hPa'
   sef['Meta']='PTC=T,PGC=T'
   sef['Data']=pandas.DataFrame(
       {'Year'  : obs_s['year'].values,
        'Month' : obs_s['month'].values,
        'Day'   : obs_s['day'].values,
        'HHMM'  : ob_hhmm,
        'TimeF' : [0] * len(obs_s),   # Instantanious
        'Value' : obs_s['value'],
        'Meta'  : [None] * len(obs_s)})

   SEF.write_file(sef,
               "%s/%s_MSLP.tsv" % (opdir,station))

