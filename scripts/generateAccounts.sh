#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
    var=${line%% *} #teil hinter dem namen wegschneiden
    var=${var,,}
    alter=$(( $RANDOM % 40 + 18 )); #random alter 18-58
    str='{"username": "'$var'","password": "'$var'","email": "'$var'@email.de","age": "'$alter'","gender": "f"}' #ausgefülltes jason mit namen
    echo $str #ausgabe
#an server senden    
curl -X POST -H "Content-Type: application/json" -d "${str}" http://rs03-db-inf-min.ad.fh-bielefeld.de:8000/users/

for i in `seq 1 10`;#random anzahl an antworten
do
str2='{"feeling": "'$(( $RANDOM % 5+1))'","activity": "'$(( $RANDOM % 5+1))'","clothing": "'$(( $RANDOM % 5+1))'","user":"'$var'"}'

#an server senden    
curl -X POST -H "Content-Type: application/json" -d "${str2}" http://rs03-db-inf-min.ad.fh-bielefeld.de:8000/questionarys/
done

done < "$1"

