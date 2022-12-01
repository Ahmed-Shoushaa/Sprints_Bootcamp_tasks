#! /bin/bash

DIR=Reports

if [ -d "$DIR" ]; then
   echo "'$DIR' has been created"
else
   mkdir ~/$DIR
fi

for month in {01..12}; do
 mkdir ~/$DIR/$month
 for day in {01..30}; do
  touch $DIR/$month/$day.xls
 done
done 

if [ $(date "+%H") -ge 00 ] && [ $(date "+%H") -le 05 ]; then
 rsync -av Reports/ /home/ahmed/Reports_backup
fi
