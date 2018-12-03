#!/usr/bin/env python

# Make a CIF file for a single station from the raw data

import os
import pandas

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
if not args.id in station_names.CIF_ID.values:
    raise ValueError("Unrecognised station ID %s" % args.id)

station_locations=pandas.read_csv("%s/../raw_data/Positions.csv" % bindir,
                              skipinitialspace=True,quotechar="'")
if not args.id in station_locations.CIF_ID.values:
    raise ValueError("Station %s has no location" % args.id)

# Load the raw data from Juerg's spreadsheet
try:
   original_name=station_names[station_names['CIF_ID']==args.id]['As-digitised'].values[0]
   assigned_number=int(station_names[station_names['CIF_ID']==args.id]['Number'].values[0])
   station_lat=station_locations[station_locations['CIF_ID']==args.id]['lat'].values[0]
   station_lon=station_locations[station_locations['CIF_ID']==args.id]['lon'].values[0]
   station_height=station_locations[station_locations['CIF_ID']==args.id]['height'].values[0]
except IndexError:
   raise StandardError("Missing original name for %s" % args.id)
spreadsheet_file=u"%s/../raw_data/South_America_1902.%s.csv" % (bindir,original_name)
if not os.path.isfile(spreadsheet_file):
   raise StandardError("Missing file %s" % spreadsheet_file)
raw_data=pandas.read_csv(spreadsheet_file)
n_values=len(raw_data)

# Make the dataframe columns common to all variables
common=pandas.DataFrame(
       {'Station_ID'    : [args.id] * n_values,
        'Station_Number': [assigned_number] * n_values,
        'Original_Name' : [original_name] * n_values,
        'Source_Number' : [None] * n_values,
        'Lat_N'         : [station_lat] * n_values,
        'Lon_E'         : [station_lon] * n_values,
        'Alt'           : [station_height] * n_values,
        'Year'          : raw_data['YEAR'].values,
        'Month'         : raw_data['MONTH'].values,
        'Day'           : raw_data['DAY'].values,
        'Time'          : [1400] * n_values})

# Make the additional columns specific to MSLP
mslp=(raw_data.iloc[:, 5]/0.75006156130264).tolist()
mslp_f=pandas.DataFrame(
      {'Time_Flag'      : [0] * n_values,   # Instantanious
       'Variable_Number': [6] * n_values,
       'Variable_Value' : mslp,
       'Variable_Flag'  : [None] * n_values})

# Output the mslp
opdir="%s/../../../cif/Argentinian_DWR/" % bindir
if not os.path.isdir(opdir):
    os.makedirs(opdir)
file_name="%s/%s_1902_MSLP.cif" % (opdir,args.id)
op_f=pandas.concat([common,mslp_f],axis=1,sort=False)
op_f.to_csv(file_name,encoding='utf-8',index=False,sep='\t',na_rep='NA',
            columns=('Station_ID','Station_Number','Source_Number','Lat_N',
                     'Lon_E','Alt','Year','Month','Day','Time','Time_Flag',
                     'Variable_Number','Variable_Flag','Variable_Value',
                     'Original_Name'))



