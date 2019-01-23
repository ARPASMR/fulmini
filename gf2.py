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
def graf(nomefile):
    """
    Plottaggio di due immagini affiancate
    nomefile= nome del file da leggere che contiene i dati (però il file non viene letto)
    df      = dataframe (viene passato direttamente in modo da non leggere da file tutte le volte)
    RL      = variabile booleana per sapere se il plottaggio riguarda la Lombardia, altrimenti plotta sull'Italia
    riquadro= lista contenente le informazioni per la selezione dell'area
    
    """
    fig = plt.figure(num=None, figsize=(20, 9),dpi=160 )
   # read file input con dati

    #Italia
    riquadro=[36,6,48.2,19]
    #df1=df
    ax=fig.add_subplot(1,2,1,projection=ccrs.PlateCarree())
    ax.set_extent([6,19,36,48.2],crs=ccrs.PlateCarree())
       
    fname='Reg_2016_LATLON.shp'       
    shape_feature=cfeature.ShapelyFeature(Reader(fname).geometries(),ccrs.PlateCarree(),facecolor=cfeature.COLORS['land'],edgecolor='green')
    ax.add_feature(shape_feature,zorder=3)     
        #land_50m=cfeature.NaturalEarthFeature('physical',name='land',scale='10m')
        #ax.add_feature(land_50m, facecolor=cfeature.COLORS['land'])
    LAKES= cfeature.NaturalEarthFeature('physical', 'lakes', '10m', edgecolor='face', facecolor=cfeature.COLORS['water'])
    ax.add_feature(LAKES,zorder=1)
    RIVERS= cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m', edgecolor=cfeature.COLORS['water'], facecolor='none')
    ax.add_feature(RIVERS,zorder=1)
    COASTLINES= cfeature.NaturalEarthFeature('physical', 'coastline', '10m', edgecolor='black', facecolor='none')
    ax.add_feature(COASTLINES)
    #OCEAN= cfeature.NaturalEarthFeature('physical', 'ocean', '50m', edgecolor='none')
    #ax.add_feature(OCEAN)
    #STATES= cfeature.NaturalEarthFeature('cultural', 'admin_0_boundary_lines_land', '50m' )
    #ax.add_feature(STATES, edgecolor='black' )        
    
    # Regione Lombardia        
    riquadro=[44.4, 8.0,46.8,11.8]
    fname='province.shp'
    #•ax.set_extent([456387,721553,4977035,5164053])
    ax2=fig.add_subplot(1,2,2,projection=ccrs.UTM(zone=32))
    shape_feature=cfeature.ShapelyFeature(Reader(fname).geometries(),ccrs.PlateCarree(),facecolor='none',edgecolor='green')
    try:
        ax2.add_wms(wms='http://www.cartografia.servizirl.it/arcgis/services/wms/DTM5_RL_wms/MapServer/WMSServer',layers=['DTM_5X5'])
        ax2.add_feature(shape_feature)
    except:
        ax2.add_wms(wms='http://www.cartografia.servizirl.it/arcgis/services/wms/dtm20_utm_wms/MapServer/WMSServer',layers=['0'])
        print("Base 5x5 non disponibile")
    fname='Reg_2016_LATLON.shp'
    ax2.set_extent([riquadro[1],riquadro[3],riquadro[0],riquadro[2]],crs=ccrs.PlateCarree())
    shape_feature=cfeature.ShapelyFeature(Reader(fname).geometries(),ccrs.PlateCarree(),facecolor='none',edgecolor='black')
    ax2.add_feature(shape_feature,zorder=1)
   
#    print('inizio plottaggio '+ nomefile)
    plt.show()
    nomefile_out=nomefile.split('.')[0]+'.jpg'
    print(nomefile_out)
    try:
        plt.savefig(nomefile_out,dpi=160) 
    except:
        print("Figura non salvata")

    
