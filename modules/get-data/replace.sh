#!/bin/sh

sed -i -e 's/True/true/g' $1
sed -i -e 's/False/false/g' $1
sed -i -e 's/'\''/'\"'/g' $1
