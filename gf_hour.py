# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 12:20:43 2019

@author: mmussin
funzione clone della gf per plottaggio orario
->oltre a nomefile e df viene passato il numero di ore indietro che chiede
-> devo tener conto che ho due file: nomefile e quello di 24 ore prima
"""
import matplotlib
import datetime as dt
# from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import warnings
import matplotlib.cbook
import pandas as pd
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
    lista_ore    = definisce il numero di ore che viene considerato nel df
    """


    colori=['#8B008B','#C71585','#FF4500','#FFA500','#FFD700','#FFFF00']
    c='#8B008B'
    riquadro=[36,6,48.2,19]
    #df1=df

    # seleziono dal dataframe solo i dati che mi interessano: se non li ho tutti allora vado indietro
    # e carico il file di ieri
    hour=24
    data_inizio=dt.datetime.utcnow()-dt.timedelta(hours=hour)
    # controllo se la data_inizio va a ieri: se sì, carico il file e lo metto nel df
    nomefile_ieri=data_inizio.strftime('%Y%m%d')+'.dat'
    if (nomefile_ieri != nomefile):
        df0=pd.read_csv(filepath_or_buffer=nomefile_ieri,sep='\s+',names=['date','time','lat','lon','int','unit','ground'],parse_dates={'datetime':['date','time']})
        df=pd.concat([df0,df])

    lista_ore=[24,6,3,1]
    df1=df[(df.lat>riquadro[0]) & (df.lat<riquadro[2]) & (df.lon>riquadro[1]) & (df.lon<riquadro[3])]
    for h in lista_ore:
        # formattazione della figura
        fig = plt.figure(num=None, figsize=(16,7 ),dpi=160 )
        #formattazione del primo subplot: Italia
        ax=fig.add_subplot(1,2,1,projection=ccrs.PlateCarree())
        ax.set_extent([6,19,36,48.2],crs=ccrs.PlateCarree())
        plt.suptitle(f"Fulmini totali dal giorno {nomefile.split('.')[0]} alle {dt.datetime.utcnow().strftime('%H:%M UTC')} indietro -{h}" , fontsize=16)
        data_inizio=dt.datetime.utcnow()-dt.timedelta(hours=h)
        lats=df1.lat[(df1.datetime>=data_inizio) & (df1.ground=='G')]
        lons=df1.lon[(df1.datetime>=data_inizio) & (df1.ground=='G')]
        lats_c=df1.lat[(df1.datetime>=data_inizio) & (df1.ground=='C')]
        lons_c=df1.lon[(df1.datetime>=data_inizio) & (df1.ground=='C')]
        try:
            ultimo_dato=df1.datetime.iloc[-1].strftime('%H:%M')
        except:
            ultimo_dato="Nessun dato"

        ax=fig.add_subplot(1,2,1,projection=ccrs.PlateCarree())
        ax.set_extent([6,19,36,48.2],crs=ccrs.PlateCarree())

            #land_50m=cfeature.NaturalEarthFeature('physical',name='land',scale='10m')
            #ax.add_feature(land_50m, facecolor=cfeature.COLORS['land'])
        fname='Reg_2016_LATLON.shp'
        shape_feature=cfeature.ShapelyFeature(Reader(fname).geometries(),ccrs.PlateCarree(),facecolor=cfeature.COLORS['land'],edgecolor='green')
        ax.add_feature(shape_feature,zorder=-1)
        LAKES= cfeature.NaturalEarthFeature('physical', 'lakes', '10m', edgecolor='face', facecolor=cfeature.COLORS['water'])
        #ax.add_feature(LAKES)
        RIVERS= cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m', edgecolor=cfeature.COLORS['water'], facecolor='none')
        #ax.add_feature(RIVERS)
        COASTLINES= cfeature.NaturalEarthFeature('physical', 'coastline', '10m', edgecolor='black', facecolor='none')
        ax.add_feature(COASTLINES)
        #OCEAN= cfeature.NaturalEarthFeature('physical', 'ocean', '50m', edgecolor='none')
        #ax.add_feature(OCEAN)
        #STATES= cfeature.NaturalEarthFeature('cultural', 'admin_0_boundary_lines_land', '50m' )
        #ax.add_feature(STATES, edgecolor='black' )
        img_extent = (6,19,36,48.2)
        img = plt.imread("mappa_sfondo.jpg")
        ax.imshow(img,origin='upper',extent=img_extent, transform=ccrs.PlateCarree())
        numero_fulmini=[]
        try:
               ax.plot(lons,lats,color=c,marker='+',markersize=4,linestyle='',zorder=1)
               ax.plot(lons_c,lats_c,color=c,marker='.',markersize=4,linestyle='',zorder=1)
        except:
               print("Problema plottaggio")
        #numero_fulmini.append(df1.lat[(df.datetime.dt.hour>=h) & (df1.datetime.dt.hour<=h+4-1) & (df1.ground=='G')].count())

        #axin=inset_axes(ax,width="12%",height="12%",loc=3)
        #axin.bar([4,8,12,16,20,24],numero_fulmini, width=2,color=colori,tick_label=[4,8,12,16,20,24])
        #axin.tick_params(axis='y',direction='in')
        #axin.grid(b=True, axis='y')
        ax.set_title(' (ultimo dato:'+ultimo_dato+')',fontdict = {'fontsize' : 14})


        # Regione Lombardia
        riquadro=[44.2, 8.0,47.1,11.8]
        df2=df[(df.lat>riquadro[0]) & (df.lat<riquadro[2]) & (df.lon>riquadro[1]) & (df.lon<riquadro[3])]
        try:
            ultimo_dato=df2.datetime.iloc[-1].strftime('%H:%M')
        except:
            ultimo_dato="Nessun dato"
        ax2=fig.add_subplot(1,2,2,projection=ccrs.UTM(zone=32))

        numero_fulmini=[]
        lats=df2.lat[(df2.datetime>=data_inizio) & (df2.ground=='G')]
        lons=df2.lon[(df2.datetime>=data_inizio) & (df2.ground=='G')]
        lats_c=df2.lat[(df2.datetime>=data_inizio) & (df2.ground=='C')]
        lons_c=df2.lon[(df2.datetime>=data_inizio) & (df2.ground=='C')]
        try:
               ax2.plot(lons,lats,color=c,marker='+',linestyle='',transform=ccrs.PlateCarree())
               ax2.plot(lons_c,lats_c,color=c,marker='.',linestyle='',transform=ccrs.PlateCarree())
        except:
               print("Problema plottaggio RL")
        numero_fulmini.append(df2.lat[(df2.datetime.dt.hour>=h) & (df2.datetime.dt.hour<=h+4-1) & (df2.ground=='G')].count())

        fname='province.shp'
        #ax.set_extent([456387,721553,4977035,5164053])
        shape_feature=cfeature.ShapelyFeature(Reader(fname).geometries(),ccrs.PlateCarree(),facecolor='none',edgecolor='green')
        try:
            ax2.add_wms(wms='http://www.cartografia.servizirl.it/arcgis/services/wms/DTM5_RL_wms/MapServer/WMSServer',layers=['DTM_5X5'])
            ax2.add_feature(shape_feature)
        except:
            print("WMS RL non disponibile")
            ax2.add_wms(wms='http://www.cartografia.servizirl.it/arcgis/services/wms/dtm20_utm_wms/MapServer/WMSServer',layers=['0'])
        fname='Reg_2016_LATLON.shp'
        ax2.set_extent([riquadro[1],riquadro[3],riquadro[0],riquadro[2]],crs=ccrs.PlateCarree())
        shape_feature=cfeature.ShapelyFeature(Reader(fname).geometries(),ccrs.PlateCarree(),facecolor='none',edgecolor='black')
        ax2.add_feature(shape_feature,zorder=1)
        #axin=inset_axes(ax2,width="12%",height="12%",loc=3)
        #axin.bar([4,8,12,16,20,24],numero_fulmini, width=2,color=colori,tick_label=[4,8,12,16,20,24])
        #axin.tick_params(axis='y',direction='in')
        #axin.grid(b=True, axis='y')
        ax2.set_title(' (ultimo dato:'+ultimo_dato+')',fontdict = {'fontsize' : 14})

    #    print('inizio plottaggio '+ nomefile)
        plt.show()
        #df2.to_csv(path_or_buf=nomefile.split('.')[0]+'_RL.dat',header=False,index=False)
        #qui va aggiunta la parte di scrittura nel dbFULMINI
        nomefile_out=nomefile.split('.')[0]+'_'+str(h)+'.png'
        print(nomefile_out)
        try:
            plt.savefig(nomefile_out,dpi=160)
        except:
            print("Figura non salvata")
    # fine ciclo su lista_ore
