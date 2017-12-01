from math import *
from random import randint

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ZeroDivisionError
    else:
        return x % m


class AJPS_instance(object):
	def __init__(self, n):
		self.n = n
		self.N = 2**n - 1
		self.w =  int(floor(sqrt(n)/2))

	def sample_low_hw(self):
		indices = []
		val = 0
		count = 0
		while count < self.w:
			i = randint(0, self.n-1)
			if i in indices:
				continue
			count += 1
			indices += [i]
			val += 2**i
		return val

	def inv(self, X):
		return modinv(X, self.N)

	def key_gen(self):
		F = self.sample_low_hw()
		G = self.sample_low_hw()
		try:
			self.inv(F)
			H = (F * self.inv(G)) % self.N
		except ZeroDivisionError:
			return self.key_gen()
		return H, F, G


	def lower_part(self, x):
		return (x % self.N) % (2**(self.n/2))

	def upper_part(self, x):
		return x - self.lower_part(x)