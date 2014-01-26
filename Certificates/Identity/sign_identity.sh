#!/bin/sh

if [ $# -ne 3 -o "$1" == "-h" ]; then
    echo "USAGE: $0 IDENTITY MDMKEY MDMCRT"
    exit 0
fi

if [ ! -f $1/$1.csr ]; then
    echo "[Error] No CSR file found in the $1 directory"
    exit 1
fi

python mdm-vendor-tool/mdm_vendor_sign.py --csr $1/$1.csr --key $2 --mdm $3
mv plist_encoded $1
    #cd mdm-vendor-tool && \
    #python mdm_vendor_sign.py --key ./vendor.key.nopass --csr ../$1/$1.csr --mdm ./mdm.cer && \
    #mv plist_encoded ../$1/
