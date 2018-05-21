#!/usr/bin/env python
#======================================
#Jeremias Pretto
#Given p, q, e in decimal
#generates RSA private and public keys

import sys
import time
import subprocess
import os

helptext = """
Se creo asn1.conf
openssl asn1parse -genconf asn1.conf  -out key.der
"""

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
       q, r = b//a, b%a
       m, n = x-u*q, y-v*q
       b,a, x,y, u,v = a,r, u,v, m,n
    return b, x, y

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
       return None  # modular inverse does not exist
    else:
       return x % m
#########################

def build_key(p,q,e):
    n = p * q
    phi = (p-1) * (q-1)
    d = modinv(e, phi)
    
    e1 = d % (p-1)
    e2 = d % (q-1)
    c = modinv(q,p)

    return (n,e,d,p,q,e1,e2,c)

def get_asn1conf(key):
# Sample config from openssl.org's ASN1_generate_nconf
    return """
asn1=SEQUENCE:private_key

[private_key]
version=INTEGER:0
n=INTEGER:%s
e=INTEGER:%s
d=INTEGER:%s
p=INTEGER:%s
q=INTEGER:%s
exp1=INTEGER:%s
exp2=INTEGER:%s
coeff=INTEGER:%s
""" % key

def main():
    if len(sys.argv) != 4:
        sys.stderr.write('Usage: %s p q e\n' % sys.argv[0])
        sys.exit(1)

    p, q, e = [ int(a,10) for a in sys.argv[1:] ]

    conf = get_asn1conf( build_key(p,q,e) )
    tiempo="output_"+str(int(time.time()))
    
    os.mkdir(tiempo)
    a= open(tiempo+'/asn1.conf','w').write(conf)
    
    subprocess.check_output('openssl asn1parse -genconf '+tiempo+'/asn1.conf  -out '+tiempo + '/privkey.der', shell=True)

#    sys.stderr.write(helptext)
#    print 'Se genero clave privada RSA en formato key'+ tiempo + '.der\n\n'

#    print 'Chequear clave'
#    print 'openssl rsa -in key'+ tiempo + '.der -inform der -text -check'

    subprocess.check_output('openssl rsa -inform DER -in '+ tiempo + '/privkey.der > '+ tiempo + '/key.priv', shell=True)


    subprocess.check_output('openssl rsa -in ' + tiempo + '/key.priv -pubout > ' + tiempo + '/key.pub', shell=True)
    
    print ("\nOutput folder: "+tiempo+"\n")
    print ("/asn1.conf:    asn1parse file (for openssl)")
    print ('/privkey.der:  RSA private key in DER format')
    print ('/key.priv:     RSA private key in b64')
    print ('/key.pub:      RSA Public key in b64')


if __name__ == "__main__":
    main()
