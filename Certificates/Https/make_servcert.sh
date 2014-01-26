#!/bin/sh

NAME=$1
CACERT=$2
CAKEY=$3

if [ -z "$CACERT" -o -z "$CAKEY" -o "$CACERT" == "-h" ]; then
    echo "USAGE: $0 -h | NAME CACERT CAKEY"
    exit 1
fi

if [ ! -d "$NAME" ]; then
    mkdir $NAME
fi

( cd $NAME && \
openssl genrsa 2048 > server.key && \
openssl req -new -key server.key -out server.csr && \
openssl x509 -req -days 365 -in server.csr -CA ../$CACERT -CAkey ../$CAKEY -CAcreateserial -out server.crt )
