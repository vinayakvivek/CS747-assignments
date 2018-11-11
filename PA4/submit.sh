#!/bin/bash

DIR=150050098
mkdir $DIR
cp -r envs $DIR
cp README.md $DIR
cp sarsa.py $DIR
cp windy_grid.py $DIR
cp utils.py $DIR
cp report.pdf $DIR

tar -cvzf $DIR.tar.gz $DIR
rm -rf $DIR