#!/bin/bash

openssl req -newkey rsa:4096 -nodes -sha256 -keyout certs/domain.key -x509 -days 365 -out certs/domain.crt -addext subjectAltName="IP:10.0.2.15" # experimentar, em vez do IP meter um DNS

mkdir -p /etc/docker/certs.d/10.0.2.15
cp certs/domain.crt /etc/docker/certs.d/10.0.2.15/ca.crt

#docker rm -f registry

docker run -d --restart=always --name registry -v "$(pwd)"/certs:/certs \
        -e REGISTRY_HTTP_ADDR=0.0.0.0:443 \
        -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
        -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
        -p 443:443 \
        registry:2
