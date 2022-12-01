#!/bin/bash 

read -p "Enter file bath you want to check it's existence:" file

while [ ! -f $file ]; 
do
 sleep 2 
 echo "File doesn't exist"
 touch $file 
 sleep 1
done 
echo "file exists"
