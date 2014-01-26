#!/bin/sh

if [ $# -lt 1 -o "$1" == "-h" ]; then
    echo "USAGE: make_identity.sh IDENTITY [CACERT CAKEY]"
    exit 1
fi

if [ ! -d "$1" ]; then
    mkdir $1
fi

function sign_csr() {
    cd $1 && \
      echo "******* Sign the CSR with CA" && \
      openssl x509 -req -days 3650 -in $1.csr -CA ../$2 -CAkey ../$3 -CAcreateserial -out $1.crt && \
      echo "******* Generate a PKCS12 certificate for the identity you have given before" && \
      openssl pkcs12 -export -out $1.p12 -inkey $1.key -in $1.crt -certfile ../$2
}

( cd $1 && \
  echo "******* Generate the privat key" && \
  openssl genrsa -des3 -out $1.key 2048 && \
  echo "******* Generate the CSR" && \
  openssl req    -new -key $1.key -out $1.csr && \
  echo "******* Remove the password" && \
  openssl rsa -in $1.key -out $1.key.nopass
)

if [ -n "$2" -a -n "$3" ]; then
    if [ ! -f "$2" -o ! -f "$3" ]; then
        echo "[Error] No files $2 or $3 found."
        exit 1
    fi

    sign_csr $1 $2 $3
fi
