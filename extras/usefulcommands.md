check private key
=================

openssl rsa -in archivo -check

Check Pub key
=============

openssl req -text -noout -verify -in CSR.csr
  
Check if pub and priv match, same md5:
======================================

openssl x509 -pubkey -in server.crt -noout | openssl md5
openssl pkey -pubout -in server.key | openssl md5
 
Same 
====

openssl x509 -noout -modulus -in server.crt| openssl md5
openssl rsa -noout -modulus -in server.key| openssl md5
 
