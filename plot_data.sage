# Create plots out of data.py

from data import c_data, q_data

first_w = {4:67, 5:101, 6:149, 7:197, 8:257, 9:100000}

def plot_time(data_set, filename):
	L = []
	for D in data_set:
		L += [(D['n'], D['time'])]

	miny = min([y for (x,y) in L])
	maxy = max([y for (x,y) in L])
	maxn = max([x for (x,y) in L])

	P = line(L, marker="+")

	for w in range(4,9):
		P += line([(first_w[w], miny), (first_w[w], maxy)],rgbcolor="black", linestyle="dashed")
		if first_w[w+1] > maxn:
			break
		if (w<8):
			P += text("$w=%d$"%w, ((first_w[w] + first_w[w+1])/2,maxy),rgbcolor="black", fontsize="large" )


	P.save(filename, scale='semilogy', aspect_ratio='automatic', axes_labels=['$n$', 'time in sec.'])

plot_time(c_data, "c_time.svg")
plot_time(q_data, "q_time.svg")

def plot_time_pred(data_set, filename):
	L = []
	for D in data_set:
		n = D['n']
		w = D['w']
		T = sqrt(binomial(n, w))
		L += [(n, T)]

	miny = min([y for (x,y) in L])
	maxy = max([y for (x,y) in L])
	maxn = max([x for (x,y) in L])

	P = line(L, marker="+")

	for w in range(4,9):
		P += line([(first_w[w], miny), (first_w[w], maxy)],rgbcolor="black", linestyle="dashed")
		if first_w[w+1] > maxn:
			break
		if (w<8):
			P += text("$w=%d$"%w, ((first_w[w] + first_w[w+1])/2,maxy),rgbcolor="black", fontsize="large" )


	P.save(filename, scale='semilogy', aspect_ratio='automatic', axes_labels=['$n$', '$\sqrt{\\binom{n}{w}}$'])

plot_time_pred(c_data, "c_time_pred.svg")


def plot_heur2(data_set, filename):
	L = []
	for D in data_set:
		L += [(D['n'], D['heur2_factor'])]

	miny = min([y for (x,y) in L])
	maxy = max([y for (x,y) in L])
	maxn = max([x for (x,y) in L])

	P = line(L, marker="+")
	P += points([(maxn, 1), (maxn, 1.3)], alpha=0)

	for w in range(4,9):
		P += line([(first_w[w], 1), (first_w[w], 1.3)],rgbcolor="black", linestyle="dashed")
		if first_w[w+1] > maxn:
			break
		if (w<8):
			P += text("$w=%d$"%w, ((first_w[w] + first_w[w+1])/2, 1.3),rgbcolor="black", fontsize="large" )


	P.save(filename, aspect_ratio='automatic', axes_labels=['$n$', '$r$\'s $9^{th}$ decile'])

plot_heur2(c_data, "c_heur2.svg")
plot_heur2(q_data, "q_heur2.svg")

def plot_succ(data_set, filename):
	L = []
	L2 = []

	for D in data_set:
		p = (1 - (2*D['w'] / (D['n']-D['b'])))**D['b']
		L += [(D['n'], D['s%'])]
		L2 += [(D['n'], p)]



	miny = min([y for (x,y) in L])
	maxy = max([y for (x,y) in L])
	maxn = max([x for (x,y) in L])

	P = line(L, marker="+")
	P += line(L2, marker="+", rgbcolor="red")
	P += points([(maxn, 0), (maxn, 1)], alpha=0)

	for w in range(4,9):
		P += line([(first_w[w], 0), (first_w[w], 1)],rgbcolor="black", linestyle="dashed")
		if first_w[w+1] > maxn:
			break
		if (w<8):
			P += text("$w=%d$"%w, ((first_w[w] + first_w[w+1])/2, 1),rgbcolor="black", fontsize="large" )


	P.save(filename, aspect_ratio='automatic', axes_labels=['$n$', 'Success rate'])

plot_succ(c_data, "c_succ.svg")
plot_succ(q_data, "q_succ.svg")