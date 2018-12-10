#!/usr/bin/env python

# Make a SEF file for a single station from the raw data

import os
import pandas
import copy
import SEF

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--id", help="Station identifier",
                    type=str,required=True)
args = parser.parse_args()

# Find the directory with this script in
try:
    bindir=os.path.abspath(os.path.dirname(__file__))
except NameError:
    bindir='.'

# Get the station metadata (names and locations)
station_names=pandas.read_csv("%s/../raw_data/names.csv" % bindir,
                              skipinitialspace=True,quotechar="'",
                              encoding='utf-8')
if not args.id in station_names.SEF_ID.values:
    raise ValueError("Unrecognised station ID %s" % args.id)

station_locations=pandas.read_csv("%s/../raw_data/Positions.csv" % bindir,
                              skipinitialspace=True,quotechar="'")
if not args.id in station_locations.SEF_ID.values:
    raise ValueError("Station %s has no location" % args.id)

# Load the raw data from Juerg's spreadsheet
try:
   original_name=station_names[station_names['SEF_ID']==args.id]['As-digitised'].values[0]
   assigned_number=int(station_names[station_names['SEF_ID']==args.id]['Number'].values[0])
   station_lat=station_locations[station_locations['SEF_ID']==args.id]['lat'].values[0]
   station_lon=station_locations[station_locations['SEF_ID']==args.id]['lon'].values[0]
   station_height=station_locations[station_locations['SEF_ID']==args.id]['height'].values[0]
except IndexError:
   raise StandardError("Missing original name for %s" % args.id)
spreadsheet_file=u"%s/../raw_data/South_America_1902.%s.csv" % (bindir,original_name)
if not os.path.isfile(spreadsheet_file):
   raise StandardError("Missing file %s" % spreadsheet_file)
raw_data=pandas.read_csv(spreadsheet_file)
n_values=len(raw_data)

# Make a SEF data structure and populate the common elements
ob_time=[700 if raw_data['MONTH'].values[i]>8 else 1400 for i in range(n_values)]
common=SEF.create(version='0.0.1')
common['ID']=args.id
common['Name']=original_name
common['Lat']=station_lat
common['Lon']=station_lon
common['Alt']=station_height
common['Source']=None
common['Repo']=None
common['Data']=pandas.DataFrame(
       {'Year'  : raw_data['YEAR'].values,
        'Month' : raw_data['MONTH'].values,
        'Day'   : raw_data['DAY'].values,
        'HHMM'  : ob_time})

# Where to put the output files
opdir="%s/../../../sef/Argentinian_DWR/" % bindir
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Tair
sef_v=copy.deepcopy(common)
sef_v['Var']='temperature'
sef_v['Units']='K'
sef_v['Data']=pandas.concat([sef_v['Data'],
                            pandas.DataFrame(
                               {'TimeF' : [0] * n_values,   # Instantanious
                                'Value' : (raw_data.iloc[:, 7]+273.15).tolist(),
                                'Meta'  : ''})],
                            axis=1,sort=False)
sef_v['Data']['Meta']=raw_data.iloc[:, 7].map(lambda(x): "Original=%dC" % x,
                                              na_action='ignore')
SEF.write_file(sef_v,
               "%s/%s_1902_T.tsv" % (opdir,args.id))

# Tmax
sef_v=copy.deepcopy(common)
sef_v['Var']='maximum temperature'
sef_v['Units']='K'
sef_v['Data']=pandas.concat([sef_v['Data'],
                            pandas.DataFrame(
                               {'TimeF' : [13] * n_values,   # Max since last
                                'Value' : (raw_data.iloc[:, 9]+273.15).tolist(),
                                'Meta'  : ''})],
                            axis=1,sort=False)
sef_v['Data']['Meta']=raw_data.iloc[:, 9].map(lambda(x): "Original=%dC" % x,
                                              na_action='ignore')
SEF.write_file(sef_v,
               "%s/%s_1902_Tmax.tsv" % (opdir,args.id))

# Tmin
sef_v=copy.deepcopy(common)
sef_v['Var']='minimum temperature'
sef_v['Units']='K'
sef_v['Data']=pandas.concat([sef_v['Data'],
                            pandas.DataFrame(
                               {'TimeF' : [13] * n_values,   # Max since last
                                'Value' : (raw_data.iloc[:, 10]+273.15).tolist(),
                                'Meta'  : ''})],
                            axis=1,sort=False)
sef_v['Data']['Meta']=raw_data.iloc[:, 10].map(lambda(x): "Original=%dC" % x,
                                              na_action='ignore')
SEF.write_file(sef_v,
               "%s/%s_1902_Tmin.tsv" % (opdir,args.id))

# RH
sef_v=copy.deepcopy(common)
sef_v['Var']='relative humidity'
sef_v['Units']='%'
sef_v['Data']=pandas.concat([sef_v['Data'],
                            pandas.DataFrame(
                               {'TimeF' : [0] * n_values,   # Instantanious
                                'Value' : (raw_data.iloc[:, 11]).tolist(),
                                'Meta'  : ''})],
                            axis=1,sort=False)
sef_v['Data']['Meta']=raw_data.iloc[:, 11].map(lambda(x): "Original=%d%%" % x,
                                              na_action='ignore')
SEF.write_file(sef_v,
               "%s/%s_1902_RH.tsv" % (opdir,args.id))


