import numpy.random
import codecs
from collections import defaultdict

scores = []

def vector3():
	return numpy.random.randint(-5, 5, 3)

def blank():
	return '__________'

def choose_random_from(v):
	if type(v)=='str':
		return v
	return v[numpy.random.randint(len(v))]


def lax_equal(x, y):
	try:
		float(x)
		return abs(x-y) <= 0.01
	except:		
		try: 
			str(x)
			return x.lower().strip()==y.lower().strip()
		except: # sloppy: assume if not float is vector
			return (abs(x-y) <= 0.01).all()

def expect_float(q):
	f = input(q)
	while True:
		try:
			return float(f)
		except ValueError:
			f = input("Invalid answer, please enter a number\n")

def expect_vector(q):
	print(q)
	v = input("Enter answer in the form x y z\n")
	while True:
		try:
			x, y, z = v.strip().split()
			return (float(x), float(y), float(z))
		except:
			v = input("Invalid answer, please answer in the form x y z\n")

def expect_categorical(q, t):
	v = input(q)
	while v.strip() not in t:
		v = input("Please enter one of the following: %s\n" % ", ".join(t))
	return v

def matrix4():
	return numpy.matrix('%d %d %d %d; %d %d %d %d; %d %d %d %d; %d %d %d %d' % tuple(numpy.random.randint(-5, 5, 16)))

def expect_matrix(q):
	print(q)
	instructions = "Please enter the matrix with columns separated by spaces and rows separated by newlines.\n"
	while True:
		try:
			print(instructions)
			ua = []
			while len(ua) < 4:
				line = input().strip().split()
				if (len(line)>0):
					ua.append(line)
			ua = numpy.matrix([[float(x) for x in elts] for elts in ua])
			if ua.shape != (4,4):
				print("Matrix must have 4 rows and 4 columns.")
				continue
			return ua
		except:
			print("Invalid input.")
		
def mxstr(m):
	"\n".join([" ".join(str(e) for e in elts) for elts in m])


def check_answer(a, ua, q, qt, eqfn=lax_equal):
	s = 0
	if eqfn(ua, a):
		print("Correct")
		s = 1
	else:
		print("Incorrect")
		print("Correct answer: ")
		print(a)
	scores.append((qt, q, a, ua, s))

def report_scores():
	qtype_score = defaultdict(float)
	qtype_count = defaultdict(int)
	for item in scores:
		(qt, q, a, ua, s) = item
		qtype_score[qt] = qtype_score[qt] + s
		qtype_count[qt] = qtype_count[qt] + 1
	for qt in qtype_score.keys():
		print("%s: %.2f (%d / %d)" % (qt, qtype_score[qt]/qtype_count[qt], qtype_score[qt], qtype_count[qt]))

def magnitude(v):
	return numpy.sqrt(v.dot(v))

def normalize(v):
	return v / magnitude(v)

def latex_preamble_str():
	return (
		r"\documentclass[11pt]{article}"
		r"\usepackage{graphicx}"
		r"\newcommand{\rmatrix}[1]{\begin{bmatrix}#1\end{bmatrix}}"
		r"\begin{document}"
		r"\begin{enumerate}"
	)

def latex_wrapup_str():
	return (
		r"\end{enumerate}\end{document}"
	)

def latex_question(q, a, params):
	pstr = ''
	if 'green' in q:		# hacky: this tells us it is picture question
		pstr = r"\includegraphics[width=0.5\textwidth]{tmp}\\"
	return r"\item %s%s" % (pstr,q), a

def generate_quiz(qtypes, n):
	with codecs.open("quiz%s.tex" % n, 'w', 'utf-8') as qfile, codecs.open("answer%s.tex" % n, 'w', 'utf-8') as afile:
		qfile.write(latex_preamble_str())
		afile.write(latex_preamble_str())
		for i in range(int(n)):
			x = numpy.random.randint(len(qtypes))
			(q, a, params) = list(qtypes.values())[x][0](False)
			qstr, astr = latex_question(q, a, params)
			qfile.write(qstr)
			afile.write(r"%s\\%s" % (qstr, astr))
		qfile.write(latex_wrapup_str())
		afile.write(latex_wrapup_str())

def getq(q, qtypes):
	if (q == "review"):
		n = input("How many questions? ")
		generate_quiz(qtypes, n)
		return
	try:
		x = numpy.random.randint(len(qtypes), size=int(q))	
		for i in x:
			list(qtypes.values())[i][0]()
	except ValueError:
		try:
			qtypes[q][0]()
		except KeyError:
			print("Invalid choice")

def main(qtypes):
	while True:
		instructions = ["'%s' for %s" % (key, value[1]) for key, value in qtypes.items()]
		q = input("Enter %s, a number n for an n-item quiz, 'review' to save a pdf quiz, or nothing to quit, and press enter \n" % ", ".join(instructions))
		if q == '':
			report_scores()
			break
		else:
			getq(q, qtypes)
