nomefile='20190118.dat'
import pandas as pd
df=pd.read_csv(filepath_or_buffer=nomefile,sep='\s+', names=['date','time','lat','lon','int','unit','ground'],parse_dates={'datetime':['date','time']})
#import gf
#gf.graf(nomefile,df)
import gf2
gf2.graf(nomefile)
