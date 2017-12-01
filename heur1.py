# Test the Heuristic 1 of the paper, up to n>20, using s samples
# usage:
# python heur1.py n s


import sys
from math import *
from ajps import AJPS_instance

n_max = int(sys.argv[1])
s = int(sys.argv[2])

def isPrime(n):
    for i in range(2,int(ceil(sqrt(n)))+1):
        if n%i==0:
            return False

    return True


def sample_heur1(inst):
	(H, F, G) = inst.key_gen()
	GX = inst.lower_part(G)
	GY = inst.upper_part(G)
	D = (H*GY % inst.N) ^ (-H*GX % inst.N)
	return bin(D).count('1')


def statistic_heur1(n, s):
	inst = AJPS_instance(n)
	L = []
	for i in range(s):
		L += [sample_heur1(inst)]
	L.sort()
	return (n, 2*inst.w, sum(L)/(1.*s), L[int(ceil(.5*s))], L[int(ceil(.9*s))])

print "dat = ["
for n in range(20, n_max):
	if not isPrime(n):
		continue
	print statistic_heur1(n, s), ","

print "]"