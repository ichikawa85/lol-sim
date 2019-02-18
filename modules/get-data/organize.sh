#!/bin/sh

dir=$1

for file in `\find $dir -name '*.json'`; do
    ./replace.sh $file
done
rm $dir/*-e 
