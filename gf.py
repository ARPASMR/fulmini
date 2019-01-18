# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 12:20:43 2019

@author: mmussin
"""
import matplotlib
import datetime as dt
# from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import warnings
import matplotlib.cbook
#from minio import Minio
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
import time
def graf(nomefile,df):
    """
    Plottaggio di due immagini affiancate
    nomefile= nome del file da leggere che contiene i dati (però il file non viene letto)
    df      = dataframe (viene passato direttamente in modo da non leggere da file tutte le volte)
    RL      = variabile booleana per sapere se il plottaggio riguarda la Lombardia, altrimenti plotta sull'Italia
    riquadro= lista contenente le informazioni per la selezione dell'area
    
    """
    fig = plt.figure(num=None, figsize=(23, 11) )
    plt.suptitle("Fulmini del giorno " + nomefile.split('.')[0]+' alle '+dt.datetime.utcnow().strftime('%H:%M UTC'), fontsize=16)
   # read file input con dati
    h=0
    colori=['#8B008B','#C71585','#FF4500','#FFA500','#FFD700','#FFFF00']

    #Italia
    riquadro=[36,6,48.2,19]
    #df1=df
    df1=df[(df.lat>riquadro[0]) & (df.lat<riquadro[2]) & (df.lon>riquadro[1]) & (df.lon<riquadro[3])]
    
    try:
        ultimo_dato=df1.datetime.iloc[-1].strftime('%H:%M')
    except:
        ultimo_dato="Nessun dato"
    ax=fig.add_subplot(1,2,1,projection=ccrs.UTM(zone=32))
    ax.set_extent([50000,1850000,4000000,5250000],crs=ccrs.UTM(zone=32))
       
        #land_50m=cfeature.NaturalEarthFeature('physical',name='land',scale='10m')
        #ax.add_feature(land_50m, facecolor=cfeature.COLORS['land'])
    LAKES= cfeature.NaturalEarthFeature('physical', 'lakes', '10m', edgecolor='face', facecolor=cfeature.COLORS['water'])
    ax.add_feature(LAKES)
    RIVERS= cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m', edgecolor=cfeature.COLORS['water'], facecolor='none')
    ax.add_feature(RIVERS)
    COASTLINES= cfeature.NaturalEarthFeature('physical', 'coastline', '10m', edgecolor='black', facecolor='none')
    ax.add_feature(COASTLINES)
    #OCEAN= cfeature.NaturalEarthFeature('physical', 'ocean', '50m', edgecolor='none')
    #ax.add_feature(OCEAN)
    STATES= cfeature.NaturalEarthFeature('cultural', 'admin_0_boundary_lines_land', '50m' )
    ax.add_feature(STATES, edgecolor='black' )        
    fname='Reg_2016_LATLON.shp'       
    shape_feature=cfeature.ShapelyFeature(Reader(fname).geometries(),ccrs.PlateCarree(),facecolor=cfeature.COLORS['land'],edgecolor='green')
    ax.add_feature(shape_feature)     
    numero_fulmini=[]
    for c in colori:
       lats=df1.lat[(df1.datetime.dt.hour>=h) & (df1.datetime.dt.hour<=h+4-1) & (df1.ground=='G')]
       lons=df1.lon[(df1.datetime.dt.hour>=h) & (df1.datetime.dt.hour<=h+4-1) & (df1.ground=='G')]
       lats_c=df1.lat[(df1.datetime.dt.hour>=h) & (df1.datetime.dt.hour<=h+4-1) & (df1.ground=='C')]
       lons_c=df1.lon[(df1.datetime.dt.hour>=h) & (df1.datetime.dt.hour<=h+4-1) & (df1.ground=='C')]
       ax.plot(lons,lats,color=c,marker='o',linestyle='',transform=ccrs.PlateCarree())
       ax.plot(lons_c,lats_c,color=c,marker='+',linestyle='',transform=ccrs.PlateCarree())
       numero_fulmini.append(df1.lat[(df1.datetime.dt.hour>=h) & (df1.datetime.dt.hour<=h+4-1) & (df1.ground=='G')].count())
       h+=4
    axin=inset_axes(ax,width="12%",height="12%",loc=3)
    axin.bar([4,8,12,16,20,24],numero_fulmini, width=2,color=colori,tick_label=[4,8,12,16,20,24])
    axin.tick_params(axis='y',direction='in')          
    axin.grid(b=True, axis='y')    
    ax.set_title(' (ultimo dato:'+ultimo_dato+')',fontdict = {'fontsize' : 14})
    
    
    # Regione Lombardia        
    riquadro=[44.2, 8.0,47.1,11.8]
    h=0
    df=df[(df.lat>riquadro[0]) & (df.lat<riquadro[2]) & (df.lon>riquadro[1]) & (df.lon<riquadro[3])]
    try:
        ultimo_dato=df.datetime.iloc[-1].strftime('%H:%M')
    except:
        ultimo_dato="Nessun dato"
    ax2=fig.add_subplot(1,2,2,projection=ccrs.UTM(zone=32))
    
    numero_fulmini=[]
    for c in colori:
       lats=df.lat[(df.datetime.dt.hour>=h) & (df.datetime.dt.hour<=h+4-1) & (df.ground=='G')]
       lons=df.lon[(df.datetime.dt.hour>=h) & (df.datetime.dt.hour<=h+4-1) & (df.ground=='G')]
       lats_c=df.lat[(df.datetime.dt.hour>=h) & (df.datetime.dt.hour<=h+4-1) & (df.ground=='C')]
       lons_c=df.lon[(df.datetime.dt.hour>=h) & (df.datetime.dt.hour<=h+4-1) & (df.ground=='C')]
       ax2.plot(lons,lats,color=c,marker='o',linestyle='',transform=ccrs.PlateCarree())
       ax2.plot(lons_c,lats_c,color=c,marker='+',linestyle='',transform=ccrs.PlateCarree())
       numero_fulmini.append(df.lat[(df.datetime.dt.hour>=h) & (df.datetime.dt.hour<=h+4-1) & (df.ground=='G')].count())
       h+=4
    fname='province.shp'
    #•ax.set_extent([456387,721553,4977035,5164053])
    shape_feature=cfeature.ShapelyFeature(Reader(fname).geometries(),ccrs.PlateCarree(),facecolor='none',edgecolor='green')
    ax2.add_wms(wms='http://www.cartografia.servizirl.it/arcgis/services/wms/DTM5_RL_wms/MapServer/WMSServer',layers=['DTM_5X5'])
    ax2.add_feature(shape_feature)
    fname='Reg_2016_LATLON.shp'
    ax2.set_extent([riquadro[1],riquadro[3],riquadro[0],riquadro[2]],crs=ccrs.PlateCarree())
    shape_feature=cfeature.ShapelyFeature(Reader(fname).geometries(),ccrs.PlateCarree(),facecolor='none',edgecolor='black')
    ax2.add_feature(shape_feature)
    axin=inset_axes(ax2,width="12%",height="12%",loc=3)
    axin.bar([4,8,12,16,20,24],numero_fulmini, width=2,color=colori,tick_label=[4,8,12,16,20,24])
    axin.tick_params(axis='y',direction='in')          
    axin.grid(b=True, axis='y')
    ax2.set_title(' (ultimo dato:'+ultimo_dato+')',fontdict = {'fontsize' : 14})
   
#    print('inizio plottaggio '+ nomefile)
    plt.show()
    df.to_csv(path_or_buf=nomefile.split('.')[0]+'_RL.dat',header=False,index=False)
    plt.savefig(nomefile.split('.')[0]+'.png',bbox_inches='tight') 

    