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

sed '42,130d; 43r ranking.html' index.html > index-aux.html
awk 'NR<42 {print}  NR==42 {system("cat ranking.html"); system("echo ");} NR>42 {print}' index-aux.html > index.html
awk -v date="$(date "+%d/%m/%y às %H:%M")" 'NR==31 {$0="<h6>última atualização: " date "</h6>"} 1' index.html > index-aux.html
mv -f index-aux.html index.html

git status >> $BS_CRAWLER_HOME/init.log
git config commit.gpgsign false
git config user.name ${AUTO_GIT_USERNAME}
git config user.email ${AUTO_GIT_EMAIL}
git add index.html ranking.html
git commit -m "[auto] atualização de placar"
git push
git config user.name ${GIT_USERNAME}
git config user.email ${GIT_EMAIL}
git config commit.gpgsign true
git config --unset user.name
git config --unset user.email

cd -