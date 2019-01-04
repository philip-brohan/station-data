#!/usr/bin/env python

# Plot and label the Argentinian DWR stations

import os
import pandas
import numpy

import matplotlib
from matplotlib.backends.backend_agg import \
             FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle

import cartopy
import cartopy.crs as ccrs

# Find the directory with this script in
try:
    bindir=os.path.abspath(os.path.dirname(__file__))
except NameError:
    bindir='.'

fig=Figure(figsize=(10,10),  # Width, Height (inches)
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
        'size'   : 16}
matplotlib.rc('font', **font)

# Argentina-centred projection
projection=ccrs.RotatedPole(pole_longitude=116, pole_latitude=128.5)
scale=9
extent=[scale*-1,scale,scale*-2,scale*2]

# Map in the centre
ax_map=fig.add_axes([0.25,0.01,0.5,0.98],projection=projection)
ax_map.set_axis_off()
ax_map.set_extent(extent, crs=projection)
ax_map.background_patch.set_facecolor((0.88,0.88,0.88,1))
land_img=ax_map.background_img(name='GreyT', resolution='low')

#Full axis for station names and linking lines
ax_full=fig.add_axes([0,0,1,1])
ax_full.patch.set_alpha(0.0) 

# Load the station locations
stations=pandas.read_csv("%s/../raw_data/Positions.csv" % bindir,
                              skipinitialspace=True,quotechar="'")
# Rotate the lats and lons into projection
rp=ax_map.projection.transform_points(ccrs.PlateCarree(),
                                  stations['lon'].values,
                                  stations['lat'].values)
stations['lon']=rp[:,0]
stations['lat']=rp[:,1]

def pos_map_in_full(lat,lon):

    result={}
    aspect=2
    result['x']=0.25+0.5*((lon-(scale*-1))/(scale*2))
    result['y']=0.01+0.98*((lat-(scale*aspect*-1))/
                                       (scale*2*aspect))
    return result

# Get the left-hand half
lon_split=numpy.mean(stations['lon'])
left=stations[stations['lon']<=lon_split]
left=left.sort_values('lat',ascending=False)
i=0.0
for index, row in left.iterrows():
    ax_map.add_patch(matplotlib.patches.Circle((row['lon'],
                                                row['lat']),
                                            radius=0.1,
                                            facecolor='red',
                                            edgecolor='black',
                                            alpha=1))
    ax_full.text(0.18,0.99-0.98*(i+0.5)/len(left),
                 row['SEF_ID'][4:],
                 horizontalalignment='right',
                 verticalalignment='center',
                 size=10,
                 color='black')
    ax_full.add_patch(Circle((0.185,
                              0.99-0.98*(i+0.5)/len(left)),
                             radius=0.001,
                             facecolor=(1,0,0,1),
                             edgecolor=(0,0,0,1),
                             alpha=1))

    mp=pos_map_in_full(row['lat'],row['lon'])
    ax_full.add_line(matplotlib.lines.Line2D(
            xdata=(0.185,mp['x']),
            ydata=(0.99-0.98*(i+0.5)/len(left),mp['y']),
            linestyle='solid',
            linewidth=0.2,
            color=(1,0,0,1.0),
            zorder=1))
    i=i+1
# Right-hand half
right=stations[stations['lon']>lon_split]
right=right.sort_values('lat',ascending=False)
i=0.0
for index, row in right.iterrows():
    ax_map.add_patch(matplotlib.patches.Circle((row['lon'],
                                                row['lat']),
                                            radius=0.1,
                                            facecolor='red',
                                            edgecolor='black',
                                            alpha=1))
    ax_full.text(0.82,0.99-0.98*(i+0.5)/len(right),
                 row['SEF_ID'][4:],
                 horizontalalignment='left',
                 verticalalignment='center',
                 size=10,
                 color='black')
    ax_full.add_patch(Circle((0.815,
                              0.99-0.98*(i+0.5)/len(right)),
                             radius=0.001,
                             facecolor=(1,0,0,1),
                             edgecolor=(0,0,0,1),
                             alpha=1))

    mp=pos_map_in_full(row['lat'],row['lon'])
    ax_full.add_line(matplotlib.lines.Line2D(
            xdata=(0.815,mp['x']),
            ydata=(0.99-0.98*(i+0.5)/len(right),mp['y']),
            linestyle='solid',
            linewidth=0.2,
            color=(1,0,0,1.0),
            zorder=1))
    i=i+1

# Output as png
fig.savefig('../figures/stations_map.png')
