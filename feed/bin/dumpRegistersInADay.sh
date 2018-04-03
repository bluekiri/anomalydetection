#!/usr/bin/env bash

day=$1
echo "read,write" > $(echo "dump_$day")

echo "Dump day: $1"

message=$(curl --silent -XGET $(echo "http://clop-elasticsearch-operations.logitravelzone.local:9200/esx-$day/_search?scroll=1m") -H 'Content-Type: application/json')
size=`echo ${message} | jq '.hits.hits | length'`
id=`echo ${message} | jq --raw-output '._scroll_id'`

while [ $size -gt 0 ]
do
    message=`curl --silent -X GET "http://clop-elasticsearch-operations.logitravelzone.local:9200/_search/scroll" -H 'Content-Type: application/json' -d "{\"scroll\" : \"1m\", \"scroll_id\" : \"${id}\" }"`
    echo ${message} | jq --raw-output '.hits.hits | .[] | [._source.IORead,._source.IOWrite] | @csv'  >> "dump_${day}"
    id=`echo ${message} | jq --raw-output '._scroll_id'`
    size=`echo ${message} | jq '.hits.hits | length'`

done
