#!/usr/bin/env python

# Make the .rst files for one station

import os
import pandas
import codecs

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--id", help="Station identifier",
                    type=str,required=True)
args = parser.parse_args()

# Get the station metadata (names)
station_names=pandas.read_csv("../../../ToDo/sources/Argentinian_DWR//raw_data/names.csv",
                              skipinitialspace=True,quotechar="'",
                              encoding='utf-8')
if not args.id in station_names.SEF_ID.values:
    raise ValueError("Unrecognised station ID %s" % args.id)


opdir="./auto_stations/%s" % args.id
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Make index file
f=codecs.open("%s/index.rst" % opdir, 'w',encoding='utf-8')
ist="""\
%s
=====================================================================================

..  |map| image:: ../../../../../ToDo/sources/Argentinian_DWR/analyses/20CRv3_comparisons/figures/station_maps/%s.png


+-------------------------------+------------------------------------------------------+
|                               |                                                      |
|                               |                                                      |
|.. toctree::                   |                                                      |
|                               |                                                      |
|   Raw data <raw>              |  |map|                                               |
|                               |                                                      |
|SEF files                      |.. toctree::                                          |
|                               |   :maxdepth: 1                                       |
|.. toctree::                   |                                                      |
|   :maxdepth: 1                |   Figure source <../../station_figures/position.rst> |
|                               |                                                      |
|   Pressure <MSLP_sf>          |                                                      |
|   Temperature <T_sf>          |                                                      |
|   Tmin <Tmin_sf>              |                                                      |
|   Tmax <Tmax_sf>              |                                                      |
|   RH <RH_sf>                  |                                                      |
|                               |                                                      |
|20CRv3 comparisons             |                                                      |
|                               |                                                      |
|.. toctree::                   |                                                      |
|   :maxdepth: 1                |                                                      |
|                               |                                                      |
|   Pressure <P_cp>             |                                                      |
|   Temperature <T_cp>          |                                                      |
|                               |                                                      |
+-------------------------------+------------------------------------------------------+

""" % (args.id,args.id)
f.write(ist)
f.close()

# Raw data file
f=codecs.open("%s/raw.rst" % opdir, 'w',encoding='utf-8')
original_name=station_names[station_names['SEF_ID']==args.id]['As-digitised'].values[0]
ist="""\
%s (raw data)
======================================================

.. literalinclude:: ../../../../../ToDo/sources/Argentinian_DWR/raw_data/South_America_1902.%s.csv

""" % (args.id,original_name)
f.write(ist)
f.close()

# SEF files
ist="""\
%s (%s SEF file)
==========================================================

.. literalinclude:: ../../../../../ToDo/sef/Argentinian_DWR/1902/%s_%s.tsv

""" 
for var in ('MSLP','T','Tmax','Tmin'):
    f=codecs.open("%s/%s_sf.rst" % (opdir,var), 'w',encoding='utf-8')
    f.write(ist % (args.id,var,args.id,var))
    f.close

# MSLP comparison
ist="""\
%s (Comparison with 20CRv3 MSLP)
=================================================================

..  figure:: ../../../../../ToDo/sources/Argentinian_DWR/analyses/20CRv3_comparisons/figures/pressure_comparison/%s.png
    :width: 95%%
    :figwidth: 95%%

    Blue dots are the 20CRv3 MSLP ensemble at the location of the station (80 ensemble members, with data every three hours). Red dots are the station observations. (Once a day, at 14:00 local up to August, at 7:00 local from September 1st).

Code to make the figure
-----------------------

.. literalinclude:: ../../../../../ToDo/sources/Argentinian_DWR/analyses/20CRv3_comparisons/plot_pressure_comparison.py

This script requires pre-extracted 20CRv3 data:

.. toctree::
   :maxdepth: 1

   Extraction scripts <../../station_figures/20CR_data_extraction>

""" % (args.id,args.id)
f=codecs.open("%s/P_cp.rst" % opdir, 'w',encoding='utf-8')
f.write(ist)
f.close()

# T comparison
ist="""\
%s (Comparison with 20CRv3 Temperature)
=====================================================================

..  figure:: ../../../../../ToDo/sources/Argentinian_DWR/analyses/20CRv3_comparisons/figures/T_comparison/%s.png
    :width: 95%%
    :figwidth: 95%%

    Blue dots are the 20CRv3 2m air temperature ensemble at the location of the station (80 ensemble members, with data every three hours). Red dots are the station observations. (Once a day, at 14:00 local up to August, at 7:00 local from September 1st). Red lines join the station Tmax and Tmin observations at the same times.

Code to make the figure
-----------------------

.. literalinclude:: ../../../../../ToDo/sources/Argentinian_DWR/analyses/20CRv3_comparisons/plot_T_comparison.py

This script requires pre-extracted 20CRv3 data:

.. toctree::
   :maxdepth: 1

   Extraction scripts <../../station_figures/20CR_data_extraction>

""" % (args.id,args.id)
f=codecs.open("%s/T_cp.rst" % opdir, 'w',encoding='utf-8')
f.write(ist)
f.close()
