#!/bin/bash

DIR=150050098
mkdir $DIR
cp evaluator.sh $DIR
cp notes.txt $DIR

tar -cvzf $DIR.tar.gz $DIR
rm -rf $DIR