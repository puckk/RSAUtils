"""
Requerimientos:
gmpy2 requeriments:
	sudo apt-get install libmpc-dev  

pip install gmpy2
pip install factordb-pycli
attackrsa

Falta:
pasar de hex a int si manda varios N y/o varios C
chosen-cipher
wiener? fermat? 
"""
import subprocess
import functools
import itertools
import argparse
from factordb.factordb import FactorDB
import gmpy2









#Si se tiene todo:
def solveSimple(p,q,c,e):
	t = (p-1)*(q-1)
	n = p*q

	# returns d such that e * d == 1 modulo t, or 0 if no such y exists.
	try:
		d = gmpy2.invert(e,t)
		m = hex(pow(c,d,n))
		print ("---------hex---------")
		print (m)#[m.index('x')+1:].decode("hex")
		print ("--------ascii--------")
		
		print (m[m.index('x')+1:].decode("hex"))
	except ZeroDivisionError:
		print (".")



#Si se tiene c,n,e y n es factorizable
def withoutpq(c,n,e):
	f= subprocess.Popen("factordb "+str(n), shell=True, stdout=subprocess.PIPE).stdout.read().replace("\n","").split(" ")
	if (len(f)> 1):
		p=int(f[0])
		q=int(f[1])
		solveSimple(p,q,c,e)
	else:
		wiener(c,n,e)
	
#SETEAR VALORES SEGUN LOS PARAMETROS...
parser = argparse.ArgumentParser()
parser.add_argument('-p',  help='p value')
parser.add_argument('-q',  help='q value')
parser.add_argument('-n',  help='n value')
parser.add_argument('-c',  help='c value')
parser.add_argument('-e',  help='e value')
parser.add_argument('-int',  action="store_true", help='inputs are in base 10 (Default)')
parser.add_argument('-hex',  action="store_true", help='inputs are in hex')
global args
args = parser.parse_args()

if args.hex & args.int:
	print ("Error: Select only hex or int")
	exit(1)


if args.hex:
	if args.p:
		if args.p[0:2]=="0x":
			p= int(args.p[2:],16)
		else:
			p=int(args.p, 16)
	if args.q:
		if args.q[0:2]=="0x":
			q= int(args.q[2:],16)
		else:
			q=int(args.q, 16)
	if args.n:
		if args.n[0:2]=="0x":
			n= int(args.n[2:],16)
		else:
			n=int(args.n, 16)
	if args.c:
		if args.c[0:2]=="0x":
			c= int(args.c[2:],16)
		else:
			c=int(args.c, 16)

	if args.e:
		if args.e[0:2]=="0x":
			e= int(args.e[2:],16)
		else:
			e=int(args.e, 16)
else:
	p=args.p
	q=args.q
	n=args.n
	c=args.c
	e=args.e
		

def hastad(n,c):
	e=len(n.split(','))
	payload= "attackrsa -t hastad -c " + c + " -n " + n + " -e " + str(len(n.split(',')))
	print (payload	)
	p = subprocess.Popen(payload, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	res=""
	for line in p.stdout.readlines():
		res=res+line
	res= res[res.index('0')+2:].strip()
	if (len(res) % 2 != 0):
		res=res+"0"
	print (res.decode("hex"))



def wiener(c,n,e):
	print ("attackrsa -t wiener -c "+str(c)+ " -e " + str(e) + " -n " + str(n))
	output=subprocess.check_output("attackrsa -t wiener -c "+str(c)+ " -e " + str(e) + " -n " + str(n), shell=True)
	print (output)
	print (output[output.index('Plain text is')+16:-2].decode("hex"))
	
		

if args.p and args.q and args.e and args.c:
	solveSimple(int(p),int(q),int(c),int(e))
if args.c and args.n and args.e:
	withoutpq(int(c),int(n),int(e))
if args.n and args.c:
	if len(args.n.split(','))>1:
		hastad(args.n, args.c)
	

