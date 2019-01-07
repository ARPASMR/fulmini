# -*- coding: utf-8 -*-
# modifica con utilizzo di cartopy al posto di basemap
import matplotlib
matplotlib.use('Agg')
#from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
import matplotlib.cbook
import datetime as dt
import os
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

print('inizio lettura dati')
def gf(nomefile):
    fname='Reg_2016_LATLON.shp'
    land_50m=cfeature.NaturalEarthFeature('physical',name='land',scale='10m', facecolor=cfeature.COLORS['land'])
    LAKES= cfeature.NaturalEarthFeature('physical', 'lakes', '10m', edgecolor='face', facecolor=cfeature.COLORS['water'])
    RIVERS= cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m', edgecolor=cfeature.COLORS['water'], facecolor='none')
    COASTLINES= cfeature.NaturalEarthFeature('physical', 'coastline', '10m', edgecolor='black', facecolor='none')
    STATES= cfeature.NaturalEarthFeature('cultural', 'admin_0_boundary_lines_land', '50m', edgecolor='black', facecolor='none')
    #cfeature.NaturalEarthFeature()
    print('elaboro il giorno ' + nomefile)
    fig = plt.figure(num=None, figsize=(22, 16) )
   # read file input con dati
    df=pd.read_csv(filepath_or_buffer='.\\data\\'+nomefile+'.dat',sep='\s+',names=['date','time','lat','lon','int','unit','ground'],parse_dates=['date','time'])
    h=0
    colori=['#8B008B','#C71585','#FF4500','#FFA500','#FFD700','#FFFF00']
    ax=fig.add_subplot(111,projection=ccrs.PlateCarree())
    ax.set_extent([6.5,18.5,35,47],crs=ccrs.PlateCarree())
    #ax.add_feature(cfeature.LAND)
    #ax.add_feature(cfeature.OCEAN)
    #ax.add_feature(cfeature.COASTLINE)
    #ax.add_feature(cfeature.BORDERS, linestyle=':')
    #ax.add_feature(cfeature.LAKES, alpha=5)
    #ax.add_feature(cfeature.RIVERS)
    #ax.add_feature(cfeature.NaturalEarthFeature('physical','land','10m',edgecolor='face',facecolors=cfeature.COLORS['land']))
    #ax.add_feature(cfeature.NaturalEarthFeature('physical','lakes','10m',edgecolor='face',facecolors='blue'))
    #ax.add_feature(cfeature.NaturalEarthFeature('physical','rivers','10m',edgecolor='face',facecolors='blue'))
    shape_feature=cfeature.ShapelyFeature(Reader(fname).geometries(),ccrs.PlateCarree(),facecolor='none',edgecolor='green')
    ax.add_feature(land_50m)
    ax.add_feature(shape_feature)
    ax.add_feature(COASTLINES)
    ax.add_feature(LAKES)
    ax.add_feature(RIVERS)
    ax.add_feature(STATES)
    #ax.stock_img()
    plt.title("Fulmini del giorno " + nomefile)
    print('inizio plottaggio '+ nomefile)
    df[(df.lat>35) & (df.lat<47) & (df.lon>6.5) & (df.lon<18.5)]
    numero_fulmini=[]
    for c in colori:
       lats=df.lat[(df.time.dt.hour>=h) & (df.time.dt.hour<=h+4-1) & (df.ground=='G')]
       lons=df.lon[(df.time.dt.hour>=h) & (df.time.dt.hour<=h+4-1) & (df.ground=='G')]
       ax.scatter(lons,lats,color=c,marker='+')
       #x,y=m(lons,lats)
       #m.scatter(x,y,color=c,marker="+")
       numero_fulmini.append(df.lat[(df.time.dt.hour>=h) & (df.time.dt.hour<=h+4-1) & (df.ground=='G')].count())
       h+=4
    axin=inset_axes(ax,width="20%",height="20%",loc=3)
    axin.bar([4,8,12,16,20,24],numero_fulmini, width=2,color=colori,tick_label=[4,8,12,16,20,24])
    axin.tick_params(axis='y',direction='in')          
    axin.grid(b=True, axis='y')
    plt.savefig(nomefile+'.png',bbox_inches='tight')         
    plt.show()
def main(lo,la):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([6.5,35,18.5,47],crs=ccrs.PlateCarree())

    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)
    ax.scatter(lo,la)
    plt.show()
    
def p():
    """
    Web tile imagery
    ----------------
    
    This example demonstrates how imagery from a tile
    providing web service can be accessed.
    
    """
    import matplotlib.pyplot as plt
    
    from cartopy.io.img_tiles import StamenTerrain
    tiler = StamenTerrain()
    mercator = tiler.crs
    ax = plt.axes(projection=mercator)
    ax.set_extent([-90, -73, 22, 34])
    
    ax.add_image(tiler, 6)
    
    ax.coastlines('10m')
    plt.show()
    
    
l=os.listdir('./data')
li=[x.split('.')[0] for x in l]
for nf in li:
    gf(nf)
   

    
