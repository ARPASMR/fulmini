Importazione dei fulmini da lampinet
# Branch master
Organizzazione originale:

-> in gagliardo scarica i file da meteoranew e crea tre gruppi: i dati raw, i dati del giorno e i dati in corso di acquisizione

-> il file bash si occupa del trasferimento dei file mente il file R si occupa della creazione dei file 

# Branch lampi
Solo codice scritto in python distinto in due:

-> applicazione Flask per servire le immagini

-> acquisizione e graficazione dei dati dei fulmini: le immagini vengono salvate in minio nel buket lampinet

# Branch cartopy
Uguale a lampi ma con libreria cartopy anzichè Basemap e Python 3. anzichè 2.7

# to do
vedere issues

# requisiti
variabili del proxy fissate come:
```
http_proxy=http://<nome_utente>:<password_utente>@proxy2.arpa.local:8080
https_proxy=https://<nome_utente>:<password_utente>@proxy2.arpa.local:8080
```
