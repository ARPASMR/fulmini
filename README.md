# Descrizione
Il codice esegue un'applicazione Flask che mostra le immagini relative ai fulmini rilevati dalla rete Lampinet per diverse scadenze temporali.
Il *Dockerfile* pilota la costruzione dell'immagine tramite *dockerhub*; il container può quindi essere deployato sia in test sia in produzione.

# Importazione dei fulmini da lampinet
(versione python 3.x)
Viene eseguita direttamente dal sito FTP di Lampinet; i dati vengono scaricati in locale sul container (effimero) e salvati in Minio solo se nella Regione Lombardia. Gli stessi dati vengono salvati su dB.

# Requisiti python
-> cartopy (necessario per il plottaggio)
-> Flask (necessario per servire le mappe)

# Variabili d'ambiente
*IRIS_DB_HOST* = collocazione del db dei fulmini
*IRIS_DB_NAME* = nome del database che contiene i fulmini
*IRIS_USER_ID* = utente del dB
*IRIS_USER_PWD*= password del dB
*FTP_PASS*     = password del FTP Lampinet
Occorre anche inserire i proxy http

# Funzionamento
*gf*              : funzione per la graficazione continua delle 24h
*scarica_fulmini* : processo principale
*gf_hour*         : funzione per la graficazione dei fulmini -24,-6,-3,-1

# Architettura su swarm
*Layer7 routing host* : *hostname*.docker.arpa.local
*Service Label*       : com.docker.lb.hosts -> *hostname*.docker.arpa.local
