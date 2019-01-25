#!/usr/bin/env python

# T2m effect plot for the Argentine DWRs in 1902

import os
import math
import datetime
import numpy
import pandas
import pickle
from collections import OrderedDict

import iris
import iris.analysis

import matplotlib
from matplotlib.backends.backend_agg import \
             FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle

import cartopy
import cartopy.crs as ccrs

import Meteorographica as mg
import IRData.twcr as twcr

import SEF
import glob

# Try and get round thread errors on spice
import dask
dask.config.set(scheduler='single-threaded')

skip_stations=['DWR_Roca_Rio_N.','DWR_Sierra_Grnde',
               'DWR_Villa_Maria','DWR_Santo_Tome','DWR_Corrientes-C',
               'DWR_Santa_Fa-Cp','DWR_San_Lorenzo','DWR_Carcarana',
               'DWR_Estc_Pereyra','DWR_Puerto_Mili.']


# Date to show
year=1902
month=6
day=17
hour=18
minute=0 # obs are at 18:17 UTC, but show the field at 18:00
dte=datetime.datetime(year,month,day,hour,minute)

# Load all the Argentine DWR pressures at this time
adf=glob.glob('../../../../sef/Argentinian_DWR/1902/DWR_*_T.tsv')
obs={'Name': [], 'Latitude': [], 'Longitude': [], 'at' : []}
for file in adf:
   stobs=SEF.read_file(file)
   df=stobs['Data']
   hhmm=int("%2d%02d" % (dte.hour,17))
   at=df.loc[(df['Year'] == dte.year) & 
               (df['Month'] == dte.month) &
               (df['Day'] == dte.day) &
               (df['HHMM'] == hhmm) ]
   if at.empty: continue
   if at['Value'].values[0]==at['Value'].values[0]:
       obs['Name'].append(stobs['ID'])
       obs['Latitude'].append(stobs['Lat'])
       obs['Longitude'].append(stobs['Lon'])
       obs['at'].append(at['Value'].values[0])
obs=pandas.DataFrame(obs)

# Landscape page
aspect=16/9.0
fig=Figure(figsize=(22,22/aspect),  # Width, Height (inches)
           dpi=100,
           facecolor=(0.88,0.88,0.88,1),
           edgecolor=None,
           linewidth=0.0,
           frameon=False,
           subplotpars=None,
           tight_layout=None)
canvas=FigureCanvas(fig)
font = {'family' : 'sans-serif',
        'sans-serif' : 'Arial',
        'weight' : 'normal',
        'size'   : 14}
matplotlib.rc('font', **font)

# South America centred projection
projection=ccrs.RotatedPole(pole_longitude=120, pole_latitude=125)
scale=25
extent=[scale*-1*aspect/3.0,scale*aspect/3.0,scale*-1,scale]

# On the left - spaghetti-contour plot of original 20CRv3
ax_left=fig.add_axes([0.005,0.01,0.323,0.98],projection=projection)
ax_left.set_axis_off()
ax_left.set_extent(extent, crs=projection)
ax_left.background_patch.set_facecolor((0.88,0.88,0.88,1))
mg.background.add_grid(ax_left)
land_img_left=ax_left.background_img(name='GreyT', resolution='low')

# 20CRv3 data
at=twcr.load('tmp',dte,level=925,version='4.5.1')
aat=at.copy()
at.data=at.data-273.15
clim=pickle.load( open( "%s/simple_climatologies/20CRv3/June_1902/air.2m_4.5.1.pkl" % os.getenv('SCRATCH'), "rb" ) )
for m in range(80):
    aat.data[m,:,:]=aat.data[m,:,:]-clim.data
obs_t=twcr.load_observations_fortime(dte,version='4.5.1')

# Plot the observations
mg.observations.plot(ax_left,obs_t,radius=0.2)

# PRMSL spaghetti plot
mg.pressure.plot(ax_left,at,scale=1,type='spaghetti',
                   resolution=0.25,
                   levels=numpy.arange(-10,40,10),
                   colors='blue',
                   label=False,
                   linewidths=0.1)

# Add the ensemble mean - with labels
at_m=at.collapsed('member', iris.analysis.MEAN)
at_s=at.collapsed('member', iris.analysis.STD_DEV)
#at_m.data[numpy.where(at_s.data>1)]=numpy.nan
mg.pressure.plot(ax_left,at_m,scale=1,
                   resolution=0.25,
                   levels=numpy.arange(-10,40,10),
                   colors='black',
                   label=True,
                   linewidths=2)

mg.utils.plot_label(ax_left,
              '20CRv3',
              fontsize=16,
              facecolor=fig.get_facecolor(),
              x_fraction=0.04,
              horizontalalignment='left')

mg.utils.plot_label(ax_left,
              '%04d-%02d-%02d:%02d' % (year,month,day,hour),
              fontsize=16,
              facecolor=fig.get_facecolor(),
              x_fraction=0.96,
              horizontalalignment='right')

# In the centre - spaghetti-contour plot of scout 4.6.1
ax_centre=fig.add_axes([0.335,0.01,0.323,0.98],projection=projection)
ax_centre.set_axis_off()
ax_centre.set_extent(extent, crs=projection)
ax_centre.background_patch.set_facecolor((0.88,0.88,0.88,1))
mg.background.add_grid(ax_centre)
land_img_centre=ax_centre.background_img(name='GreyT', resolution='low')

# Load the 4.6.1 data
at2=twcr.load('air.2m',dte,version='4.6.1')
aat2=at2.copy()
at2.data=at2.data-273.15
clim=pickle.load( open( "%s/simple_climatologies/20CRv3/June_1902/air.2m_4.6.1.pkl" % os.getenv('SCRATCH'), "rb" ) )
for m in range(80):
    aat2.data[m,:,:]=aat2.data[m,:,:]-clim.data
obs_t2=twcr.load_observations_fortime(dte,version='4.6.1')

mg.observations.plot(ax_centre,obs_t2,radius=0.2)

# PRMSL spaghetti plot
mg.pressure.plot(ax_centre,at2,scale=1,type='spaghetti',
                   resolution=0.25,
                   levels=numpy.arange(-5,35,5),
                   colors='blue',
                   label=False,
                   linewidths=0.1)

# Add the ensemble mean - with labels
at_m=at2.collapsed('member', iris.analysis.MEAN)
at_s=at.collapsed('member', iris.analysis.STD_DEV)
#at_m.data[numpy.where(at_s.data>1)]=numpy.nan
mg.pressure.plot(ax_centre,at_m,scale=1,
                   resolution=0.25,
                   levels=numpy.arange(-5,35,5),
                   colors='black',
                   label=True,
                   linewidths=2)

mg.utils.plot_label(ax_centre,
              'Scout 4.6.1',
              fontsize=16,
              facecolor=fig.get_facecolor(),
              x_fraction=0.04,
              horizontalalignment='left')


# Validation scatterplot on the right
obs=obs.sort_values(by='Latitude',ascending=False)
stations=list(OrderedDict.fromkeys(obs.Name.values))
# Need obs from a wider time-range to interpolate observed pressures
interpolate_obs=obs
ax_right=fig.add_axes([0.74,0.05,0.255,0.94])
# x-axis
xrange=[-15,15]
ax_right.set_xlim(xrange)
ax_right.set_xlabel('')

# y-axis
ax_right.set_ylim([1,len(stations)+1])
y_locations=[x+0.5 for x in range(1,len(stations)+1)]
ax_right.yaxis.set_major_locator(
              matplotlib.ticker.FixedLocator(y_locations))
ax_right.yaxis.set_major_formatter(
              matplotlib.ticker.FixedFormatter(
                  [s[4:] for s in stations]))

# Custom grid spacing
for y in range(0,len(stations)):
    ax_right.add_line(matplotlib.lines.Line2D(
            xdata=xrange,
            ydata=(y+1,y+1),
            linestyle='solid',
            linewidth=0.2,
            color=(0.5,0.5,0.5,1),
            zorder=0))

latlon={}

# Plot the station pressures
for y in range(0,len(stations)):
    station=stations[y]
    try:
        at=obs[obs.Name==station]['at'].values[0]-273.15-20
    except Exception: continue 
    if at is None: continue  
    if station in skip_stations:                         
        ax_right.add_line(matplotlib.lines.Line2D(
                xdata=(at,at), ydata=(y+1.1,y+1.9),
                linestyle='solid',
                linewidth=3,
                color=(0,0,0,0.5),
                zorder=1))
    else:
        ax_right.add_line(matplotlib.lines.Line2D(
                xdata=(at,at), ydata=(y+1.1,y+1.9),
                linestyle='solid',
                linewidth=3,
                color=(0,0,0,1),
                zorder=1))

# for each station, plot the V3 ensemble at that station
interpolator = iris.analysis.Linear().interpolator(aat, 
                                   ['latitude', 'longitude'])
for y in range(len(stations)):
    station=stations[y]
    ensemble=interpolator([obs[obs.Name==station].Latitude.values[0],
                           obs[obs.Name==station].Longitude.values[0]])

    ax_right.scatter(ensemble.data,
                numpy.linspace(y+1.5,y+1.9,
                              num=len(ensemble.data)),
                20,
                'blue', # Color
                marker='.',
                edgecolors='face',
                linewidths=0.0,
                alpha=0.5,
                zorder=0.5)

# For each station, plot the scout ensemble at that station.
for y in range(len(stations)):
    station=stations[y]
    interpolator = iris.analysis.Linear().interpolator(aat2, 
                                   ['latitude', 'longitude'])
    ensemble=interpolator([obs[obs.Name==station].Latitude.values[0],
                           obs[obs.Name==station].Longitude.values[0]])
    ax_right.scatter(ensemble.data,
                numpy.linspace(y+1.1,y+1.5,
                              num=len(ensemble.data)),
                20,
                'red', # Color
                marker='.',
                edgecolors='face',
                linewidths=0.0,
                alpha=0.5,
                zorder=0.5)

# Join each station name to its location on the map
# Need another axes, filling the whole fig
ax_full=fig.add_axes([0,0,1,1])
ax_full.patch.set_alpha(0.0)  # Transparent background

def pos_left(idx):
    station=stations[idx]
    rp=ax_centre.projection.transform_points(ccrs.PlateCarree(),
                              numpy.asarray(obs[obs.Name==station].Longitude.values[0]),
                              numpy.asarray(obs[obs.Name==station].Latitude.values[0]))
    new_lon=rp[:,0]
    new_lat=rp[:,1]

    result={}
    result['x']=0.335+0.323*(new_lon-(scale*-1)*aspect/3.0)/(scale*2*aspect/3.0)
    result['y']=0.01+0.98*(new_lat-(scale*-1))/(scale*2)
    return result

# Label location of a station in ax_full coordinates
def pos_right(idx):
    result={}
    result['x']=0.668
    result['y']=0.05+(0.94/len(stations))*(idx+0.5)
    return result

for i in range(len(stations)):
    p_left=pos_left(i)
    if p_left['x']<0.335 or p_left['x']>(0.335+0.323): continue
    if p_left['y']<0.005 or p_left['y']>(0.005+0.94): continue
    p_right=pos_right(i)
    ax_full.add_patch(Circle((p_right['x'],
                              p_right['y']),
                             radius=0.001,
                             facecolor=(1,0,0,1),
                             edgecolor=(0,0,0,1),
                             alpha=1,
                             zorder=1))
    ax_full.add_line(matplotlib.lines.Line2D(
            xdata=(p_left['x'],p_right['x']),
            ydata=(p_left['y'],p_right['y']),
            linestyle='solid',
            linewidth=0.2,
            color=(1,0,0,1.0),
            zorder=1))

# Output as png
fig.savefig('T2m_Effect_%04d%02d%02d%02d%02d.png' % 
                                  (year,month,day,hour,minute))
