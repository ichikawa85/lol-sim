#!/bin/sh

version="9.6.1"

mkdir ./champions/${version}
while IFS= read line
do
    curl --request GET "http://ddragon.leagueoflegends.com/cdn/${version}/data/en_US/champion/${line%$'\r'}.json" --include > ./champions/${version}/"${line%$'\r'}.json"
    sed -i -e '1,18d' ./champions/${version}/"${line%$'\r'}.json"
    # touch src/8.24.1/${line%$'\r'}.py
done < ./champion-list.txt

rm ./champions/${version}/*-e
