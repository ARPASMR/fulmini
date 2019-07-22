# Importazione dei fulmini da lampinet
(versione python 3.x)

# Requisiti python

-> cartopy (necessario per il plottaggio)

-> Flask (necessario per servire le mappe)

# NOTA
Occorre inserire manualmente la password per il trasferimento FTP come variabili di ambiente.

Occorre anche inserire i proxy http

# uso di compose
si può usare il file .yml per creare uno stack in UCP

# forzare l'update del servizio
Nel Master1:
```
docker service update --force --image arpasmr/fulmini:cartopy Fulmini_ful
```
