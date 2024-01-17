#!/bin/bash
if [ -z "$1" ]; then
  echo "Must pass site home arg."
  exit 1
fi

if [ -z "$2" ]; then
  echo "Must pass auto commiter info. [AUTO_GIT_USERNAME]"
  exit 1
fi
if [ -z "$3" ]; then
  echo "Must pass auto commiter info. [AUTO_GIT_EMAIL]"
  exit 1
fi

if [ -z "$4" ]; then
  echo "Must pass auto commiter info. [GIT_USERNAME]"
  exit 1
fi
if [ -z "$5" ]; then
  echo "Must pass auto commiter info. [GIT_EMAIL]"
  exit 1
fi

python3 src/util/html_generator.py 
mv -f ranking.html $1/

cd $1

sed '42,131d; 43r ranking.html' index.html > index-aux.html
awk 'NR<42 {print}  NR==42 {system("cat ranking.html"); system("echo ");} NR>42 {print}' index-aux.html > index.html
awk -v date="$(date "+%d/%m/%y às %H:%M")" 'NR==31 {$0="<h6>última atualização: " date "</h6>"} 1' index.html > index-aux.html
mv -f index-aux.html index.html

git status >> $BS_CRAWLER_HOME/init.log
git config commit.gpgsign false
git config user.name ${2}
git config user.email ${3}
git add index.html ranking.html
git commit -m "[auto] atualização de placar"
git push
git config user.name ${4}
git config user.email ${5}
git config commit.gpgsign true
git config --unset user.name
git config --unset user.email

cd -