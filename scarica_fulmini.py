# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 10:12:46 2018

@author: mmussin
versione con cartopy al posto di basemap

 prendo i fulmini da lampinet
 meccanismo di alimentazione:
 1. mi collego a meteoranew tramite proxy
 2. verifico l'esistenza del file del giorno in corso AAAAMMGG.dat
 3. se il file esiste, leggo i dati e vedo quando è l'ultimo
 4. determino l'elenco dei file da leggere
 5. ciclo sui file:
    -> li trasferisco in locale
    -> leggo il df
    -> appendo il df
    -> scrivo il nuovo df
 6. plottaggio 
 7. copio su minio di ARPA

 NOTA: too many I/O may slower the process
       la funzione di plottaggio è parametrizzata
"""
# 0. Inizializzazioni
import matplotlib
matplotlib.use('Agg')
import os
import datetime as dt
import pandas as pd
from ftplib import FTP
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

HOST='meteoranew.protezionecivile.it'
USER='lombardia'
#PASS=os.getenv('FTP_PASS')
REMOTE_DIR='/lampi'
ftp=FTP()
# funzione di graficazione fulmini
import gf
# 1.
ftp.connect(host='proxy2.arpa.local',port=2121)
ftp.set_debuglevel(0)
ftp.login(USER+'@'+HOST,PASS)
elenco_file=ftp.nlst(REMOTE_DIR)
#print(elenco_file)
# se il file esiste ne leggo il contenuto
curdate=dt.datetime.utcnow()
nomefile=curdate.strftime('%Y%m%d')+'.dat'
nomeimg=nomefile.split('.')[0]+'.png'
nomeimgRL=nomefile.split('.')[0]+'_RL.png'
file_controllo='file_controllo.txt'
try:
    cntl=pd.read_csv(filepath_or_buffer=file_controllo,names=['nomefile'])
except:
    cntl=pd.DataFrame()
# 2.

    #lastdata=df.date.iloc[-1]
# 3.4.5. elenco file contiene l'elenco dei file su meteora: devo scaricare solo quelli che non ho già scaricato  

for nf in elenco_file:
    comando='RETR '+ nf
    fi=nf[16:24] #fi contiene solo AAAAMMGG
    if ((fi == curdate.strftime('%Y%m%d')) & (not(cntl.nomefile.str.contains(nf).any()))):
        fhandle=open(curdate.strftime('%Y%m%d')+'.dat','ab')
        ftp.retrbinary(comando,fhandle.write,8192)
        fhandle.close()
        cntl=cntl.append({'nomefile': nf},ignore_index=True)
cntl.to_csv(path_or_buf=file_controllo, header=False,index=False)
# read file input con dati
df=pd.read_csv(filepath_or_buffer=nomefile,sep='\s+',names=['date','time','lat','lon','int','unit','ground'],parse_dates={'datetime':['date','time']})
riquadro=[36,6,48.2,19]
riquadro_RL=[44.49, 8.10,46.9,11.6]

try: 
    gf.graf(nomefile,df,False,riquadro)
except:
    print( 'ERRORE: file '+ nomefile + ' non trovato o errore in gf') 
try:
    gf.graf(nomefile,df,True,riquadro_RL)
except:
    print('ERRORE: non riuscito plottaggio RL per '+ nomefile)   
# trasferimento a minio    
minioClient=Minio('10.10.99.135:9000',access_key='ACCESS_KEY',secret_key='SECRET_KEY',secure=False)
try:
    with open(nomeimg,'rb') as file_data:
        file_stat=os.stat(nomeimg)
        print(minioClient.put_object('lampinet',nomeimg,file_data,file_stat.st_size))
except:
    print ('something went wrong')
try:
    with open(nomeimgRL,'rb') as file_data:
        file_stat=os.stat(nomeimgRL)
        print(minioClient.put_object('lampinet',nomeimgRL,file_data,file_stat.st_size))
except:
    print ('something went wrong with RL')
