# Iterator to generate low hamming weights binary vectors


class lwh:
	def __init__(self, n, w):
		assert w <= n
		self.p = range(w)
		self.n = n
		self.w = w
		self.oldp = range(w)
		self.last = False

	def __iter__(self):
		return self

	def next(self):

		if self.last:
			raise StopIteration()
		if self.w==0:
			self.last = True
			return self.p

		for i in range(self.w):
			self.oldp[i] = self.p[i]
		j = self.w - 1
		m = 0
		while True:
			self.p[j] += 1
			if self.p[j] >= self.n - m:
				j -= 1
				m += 1
				if j < 0:
					self.last = True
					break
			else:
				break

		for k in range(j+1, self.w):
			self.p[k] = self.p[k-1] + 1

		return self.oldp

