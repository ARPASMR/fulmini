# Importazione dei fulmini da lampinet
(versione python 3.x)

# Requisiti python

-> cartopy (necessario per il plottaggio)

-> Flask (necessario per servire le mappe)

# NOTA
Occorre inserire manualmente la password per il trasferimento FTP come variabili di ambiente.

Occorre anche inserire i proxy http

# Funzionamento
gf: funzione per la graficazione continua delle 24h
scarica_fulmini: processo principale
gf_hour: funzione per la graficazione dei fulmini -24,-6,-3,-1
