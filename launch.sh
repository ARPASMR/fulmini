#!/bin/bash
# script di lancio del processo di graficazione fulmini
# prende come argomento il numero di secondi di sleeping
nomescript=${0##*/}
# lancio la parte di server
./launch_flask.sh &
if [ $1 <300 ]
then
   dormi=300
else
   dormi=$1
fi
while [ 1 ]
do
  python scarica_fulmini.py
  find -type f -ctime +7 -name "*.dat" -exec rm -vf {} \;
	find static/ -type f -ctime +7 -name "*.png" -exec rm -vf {} \;
  find static/ -type f -ctime +1 -name "*_?.png" -exec rm -vf {} \;
  find static/ -type f -ctime +1 -name "*_??.png" -exec rm -vf {} \;
	mv *.png ./static/
        ps -ef|grep mostra_fulmini|grep -v grep|awk '{print $2}'|xargs kill -9
	ls -L ./static/*.png > ./static/fof.txt
	./launch_flask.sh &
        sleep 300
done
