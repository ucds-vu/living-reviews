#! /bin/sh
curl -L -H "Accept: text/turtle" $1 > ./doi/$2.ttl
