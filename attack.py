# Run the attack, up to dimension n_max, with s sample
# usage:
# python attack.py n s          (classical)
# python attack.py n s q        (quantum)

import sys
from math import *
from ajps import AJPS_instance
from lhw_iter import lwh
from random import randint
from time import time
from collections import OrderedDict

max_n = int(sys.argv[1])
samples = int(sys.argv[2])

def isPrime(n):
    for i in range(2, int(ceil(sqrt(n)))+1):
        if n%i==0:
            return False
    return True


print "samples = %d"%samples

quantum=False

try:
    if sys.argv[3]=="q":
        quantum = True
except:
    pass

if quantum:
    print "QUANTUM"
else:
    print "CLASSICAL"


def nCr(n, r):
    return factorial(n) / factorial(r) / factorial(n-r)


class AJPS_attack(object):
    def __init__(self, n, H, quantum=False):
        self.n = n
        self.N = 2**n - 1
        self.H = H
        self.w =  int(floor(sqrt(n)/2))
        self.Hrot = n*[0]

        for i in range(n):
            self.Hrot[i] = H
            H = (2 * H) % self.N
        


        if not quantum:
            self.wX = self.w/2
            self.nX = self.n/2
            self.nY = self.n - self.nX
            self.wY = self.w - self.wX
            if self.wX < self.wY:
                while nCr(self.nX, self.wX) < nCr(self.nY, self.wY):
                    self.nX += 1
                    self.nY -= 1
        else:
            self.wX = (self.w + 2)/3
            self.nX = self.n/3
            self.nY = self.n - self.nX
            self.wY = self.w - self.wX
            while nCr(self.nX, self.wX)**2 < nCr(self.nY, self.wY):
                    self.nX += 1
                    self.nY -= 1

        self.b = int(floor(log(nCr(self.nX, self.wX))/log(2))) 

        self.b_mask = 2**self.b - 1

        # print "wX, wY :",
        # print self.wX, self.wY, 
        # print "nX, nY :",
        # print self.nX, self.nY,
        # print "b = ", self.b

        # if not self.optimized:
        #    self.h_indices = [randint(0, n-1) for i in range(self.b)]

    def h(self, A):
        res = 0
        for i in range(self.b):
            res *= 2
            res += int((A >> i) & 1)
        return res

    def GXH(self, I):
        res = 0
        for i in I:
            res += self.Hrot[i]
        return res % self.N

    def GYH(self, I):
        res = 0
        for i in I:
            res += self.Hrot[i + self.wX]
        return res % self.N

    def attack(self):
        collisions = 0
        database = [[] for i in range(2**self.b)]
        sol_F = None
        for IX in lwh(self.nX, self.wX):
            vGXH = self.GXH(IX)
            hGXH = self.h(vGXH)
            database[hGXH] += [vGXH]

        for IY in lwh(self.nY, self.wY):
            vGYH = self.GYH(IY)
            hGYH = self.h((-vGYH) % self.N)
            for vGXH in database[hGYH]:
                collisions += 1
                S = (vGXH + vGYH) % self.N
                if bin(S).count('1') <= self.w:
                    sol_F = S

        return sol_F, collisions


def test_attack(n, quantum):
    inst = AJPS_instance(n)
    H, F, G = inst.key_gen()
    attacker = AJPS_attack(n, H, quantum=quantum)
    F2, collisions = attacker.attack()
    pred_coll =  nCr(attacker.nX, attacker.wX) * nCr(attacker.nY, attacker.wY) / (2.**attacker.b)

    succ = False
        
    if F2 is not None:
        G2 = F2 * inst.inv(H) % (2**n - 1)
        FoF2 = G2 * inst.inv(G) % (2**n - 1)
        if bin(FoF2).count('1') == 1:
            succ += True
    return succ, collisions/pred_coll


def print_dict(D):
    print "{",
    for a in D:
        if isinstance(D[a], int):
            print "'%s':%4d,"%(a, D[a]),
        else:
            print "'%s':%.4f,"%(a, D[a]),
    print "}"



for n in range(20, max_n):
    if not isPrime(n):
        continue
    inst = AJPS_attack(n, 0, quantum=quantum)

    # print
    # print "wX, wY :",
    # print inst.wX, inst.wY, 
    # print "nX, nY :",
    # print inst.nX, inst.nY,
    # print "b = ", inst.b
    START = time()
    nb_succ = 0
    col_ratios = []
    for k in range(samples):
        succ, col_ratio = test_attack(n, quantum=quantum)
        nb_succ += succ
        col_ratios += [col_ratio]
    col_ratios.sort()
    TIME = time() - START
    D = OrderedDict()
    D["n"] = inst.n
    D["w"] = inst.w
    D["b"] = inst.b
    D["trials"] = samples
    D["s%"] = nb_succ/(1. * samples)
    D["time"] = TIME/(1. * samples)
    D["heur2_factor"] = col_ratios[90*samples/100 -1]
    D["quantum"] = quantum

    print_dict(D)

