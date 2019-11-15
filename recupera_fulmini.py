# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 10:12:46 2018

@author: mmussin
versione con cartopy al posto di basemap
--> recupero dei fulmini su minio
 
 meccanismo di alimentazione:
 1. stabilisco l'intervallo di date da recuperare    
 2. verifico l'esistenza del file del giorno in corso AAAAMMGG_RL.dat
 3. se il file esiste, copio da minio
 4. ciclo di importazione nel db

 
"""
# 0. Inizializzazioni

import os
import datetime as dt
import pandas as pd
# import numpy as np
from sqlalchemy import *
from minio import Minio


# 1.
data_iniziale='2019-01-01'
data_finale='2019-11-10'
elenco=pd.date_range(data_iniziale,data_finale)
minioClient=Minio('10.10.99.135:9000',access_key='ACCESS_KEY',secret_key='SECRET_KEY',secure=False)
for giorno in elenco:
    nomefile=giorno.strftime('%Y%m%d')+'_RL.dat'
    try:
        data=minioClient.get_object('lampinet',nomefile)
        with open('fulmini_all.csv','ab+') as file_data:
            for d in data:
                file_data.write(d)
    except :
        print (f'something went wrong with minio: ')
# 2.

    #lastdata=df.date.iloc[-1]
# 3.4.5. elenco file contiene l'elenco dei file su meteora: devo scaricare solo quelli che non ho già scaricato  



# trasferimento a minio    


# trasferimento al dB


IRIS_USER_ID='postgres'
IRIS_USER_PWD='p0stgr3S'
IRIS_DB_NAME='fulmini'
IRIS_DB_HOST='10.10.0.19'
IRIS_SCHEMA_NAME='public'
engine = create_engine('postgresql+pg8000://'+IRIS_USER_ID+':'+IRIS_USER_PWD+'@'+IRIS_DB_HOST+'/'+IRIS_DB_NAME)
conn=engine.connect()
nf='fulmini_all.csv'
df=pd.read_csv(nf,sep=',',header=None,names=['data_e_ora','lat','lon','int','unit','ground'])
sql = '''\
INSERT INTO public.stroke (data_e_ora, int, ground, geometry) 
VALUES(%s,%s,%s,ST_SetSRID(ST_MakePoint(%s, %s), 4326));
'''
for i in df.itertuples():
    vars=[i.data_e_ora,i.int,i.ground,i.lon,i.lat]
    try:
       conn.execute(sql, vars)
       print("insert")
    except:
        print(f"ERRORE: inserimento non riuscito per {i.data_e_ora}")
