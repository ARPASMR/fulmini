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


# 1.
data_iniziale='2018-08-10'
data_finale='2019-01-26'
elenco=pd.date_range(data_iniziale,data_finale)

IRIS_USER_ID='postgres'
IRIS_USER_PWD='p0stgr3S'
IRIS_DB_NAME='fulmini'
IRIS_DB_HOST='10.10.0.19'
IRIS_SCHEMA_NAME='public'
engine = create_engine('postgresql+pg8000://'+IRIS_USER_ID+':'+IRIS_USER_PWD+'@'+IRIS_DB_HOST+'/'+IRIS_DB_NAME)
conn=engine.connect()
nf='fulmini_all.csv'
for giorno in elenco:
    try:
        nf=giorno.strftime('%Y%m%d')+'.dat'
        df1=pd.read_csv(nf,sep=' ',header=None,names=['date','time','lat','lon','int','unit','ground'],parse_dates={'data_e_ora':['date','time']})
        df=df1.query('lat > 36 and lat < 48.2 and lon> 6 and lon < 19')
        sql = '''\
        INSERT INTO public.stroke (data_e_ora, int, ground, geometry) 
        VALUES(%s,%s,%s,ST_SetSRID(ST_MakePoint(%s, %s), 4326));
        '''
        for i in df.itertuples():
            vars=[i.data_e_ora,i.int,i.ground,i.lon,i.lat]
            try:
                conn.execute(sql, vars)
                #print(sql)
            except:
                print(f"ERRORE: inserimento non riuscito per {i.data_e_ora}")
    except:
        print(f"file {nf} non esiste")
