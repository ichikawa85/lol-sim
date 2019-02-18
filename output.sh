#!/bin/sh

version="9.3.1"

curl --request GET "http://ddragon.leagueoflegends.com/cdn/${version}/data/en_US/champion.json" --include > ./champions/${version}-champions.json
sed -i -e '1,18d' ./champions/${version}-champions.json
