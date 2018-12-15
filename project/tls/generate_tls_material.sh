#openssl genrsa -des3 -out ca.key 4096
#openssl req -new -x509 -days 99999 -key ca.key -out ca.crt

#openssl genrsa -out server.key 4096
openssl req -new -out server.csr -key server.key
# openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 99999
openssl x509 -req -in server.csr \
        -extfile <(printf "subjectAltName=IP:172.28.1.1") \
        -CA ca.crt \
        -CAkey ca.key \
        -CAcreateserial -out server.crt \
        -days 365