# RSAUtils

rsabuilder
==========

Script to create public and private key via openssl using "p", "q" and "e" in decimal value


Example:

Generate RSA keys with p=61, q=53 and e=17

```
$ cd 01-rsabuilder/
$ python rsabuilder.py 61 53 17
```

**Output folder**: output_1526911937

*/asn1.conf*:    asn1parse file (for openssl)

*/privkey.der*:  RSA private key in DER format

*/key.priv*:     RSA private key in b64

*/key.pub*:      RSA Public key in b64



rsactfsolver
============

In Process...
