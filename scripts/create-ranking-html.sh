#!/bin/bash
if [ -z "$1" ]; then
  echo "Must pass site home arg."
  exit 1
else
  echo "1: $1"
fi

python3 src/util/html_generator.py 
mv -f ranking.html $1/

cd $1

sed '52,141d; 53r ranking.html' index.html > index-aux.html
awk 'NR<52 {print}  NR==52 {system("cat ranking.html"); system("echo ");} NR>52 {print}' index-aux.html > index.html
awk -v date="$(date "+%d/%m/%y às %H:%M")" 'NR==33 {$0="<h3>Última atualização: " date "</h3>"} 1' index.html > index-aux.html
mv -f index-aux.html index.html

git status >> $BS_CRAWLER_HOME/init.log
git add index.html ranking.html
git commit -m "[auto] atualização de placar"
git push

cd -