import numpy
import codecs
from collections import defaultdict
import graphicsFunctions as gf
import csv
import re

scores = []

test_strings = [0.321, """[[ 0.          0.70710678 -0.70710678  4.        ]
  [ 0.94280904 -0.23570226 -0.23570226 -1.        ]
  [-0.33333333 -0.66666667 -0.66666667 -4.        ]
  [ 0.          0.          0.          1.        ]]""", "[-0.33333333 -0.66666667 -0.66666667 -4.        ]", [numpy.random.random() for i in range(10)], [[numpy.random.random() for j in range(4)] for i in range(4)]]

with open('unit_ish_vectors.csv', 'r') as f:
	directions = list(csv.reader(f))[1:]	# skip header
	directions = [[float(f) for f in line] for line in directions]

def vector3():
	return numpy.random.randint(-5, 5, 3)

def vector(n=3):
	return numpy.random.randint(-5, 5, n)

def color():
	c = vector3()
	if (max(c)==0):
		c[numpy.random.randint(len(c))]=1
	return numpy.array([round(abs(cc/max(c)), 1) for cc in c])

def direction():
	d = numpy.array(choose_random_from(directions)[0:3])
	print("Note: to simplify calculations, directions are chosen to have components of only two decimal places and magnitudes very close (within 0.001) to 1. You can treat them in your calculations as unit vectors.")
	return numpy.random.permutation(d)

def blank():
	return '__________'

def choose_random_from(v):
	if type(v)=='str':
		return v
	return v[numpy.random.randint(len(v))]

def tostring(x):
	return numpy.array_str(numpy.array(x))

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

def expect_vector(q, dim=3):
	print(q)
	v = input("Enter answer in the form %s\n" % ' '.join(["v%d" % i for i in range(dim)]))
	while True:
		try:
			elts = v.strip().split()
			return [float(e) for e in elts]
		except:
			v = input("Invalid answer, please answer in the form %s\n" % ' '.join(["v%d" % i for i in range(dim)]))

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


def latex_preamble_str():
	return (
		r"\documentclass[11pt]{article}"
		r"\usepackage{graphicx}"
		r"\usepackage[margin=1in]{geometry}"
		r"\usepackage{underscore}"
    r"\usepackage{amsmath}"
		r"\newcommand{\rmatrix}[1]{$\begin{bmatrix}#1\end{bmatrix}$}"
		r"\begin{document}"
		r"\begin{enumerate}"
	)

def latex_wrapup_str():
	return (
		r"\end{enumerate}\end{document}"
	)

def list_to_latex(m):
  if len(numpy.array(m).shape)==1:
    m = [m]
  if isinstance(m, numpy.matrix):
    m = m.tolist()
  return r"\rmatrix{%s}" % r'\\'.join('&'.join(str(numpy.round(ac, 2)) for ac in a) for a in m)

def array_str_to_latex(s):
  return list_to_latex([float(ac) for a in re.compile(r"(\[.+?\])").findall(s) for ac in a.replace('[','').replace(']', '').split()])

def array_regex_to_latex(mg):
	return array_str_to_latex(mg.group(0))

def latex_clean_str(s):
  return s.replace("\n", '')

def latex_clean(s):
  try:
    return str(round(float(s), 2))
  except:
    if isinstance(s, list) or isinstance(s, tuple):
      return " OR ".join(s)
    if isinstance(s, numpy.ndarray):
      return list_to_latex(s)
    if isinstance(s, str):
      s = s.replace("\n", '')
      return re.sub(r"(?P<array>\[.+?\])", array_regex_to_latex, s)
    print("error: type not handled")
    print(type(s))
    print(s)

def latex_question(q, a, params):
  pstr = ''
  if 'green' in q:		# hacky: this tells us it is picture question
    pstr = r"\includegraphics[width=0.5\textwidth]{tmp}\\"
  return r" \item %s%s" % (pstr,latex_clean(q)), r" \item %s" % latex_clean(a)

def generate_quiz(qtypes, n):
	with codecs.open("quiz%s.tex" % n, 'w', 'utf-8') as qfile, codecs.open("answer%s.tex" % n, 'w', 'utf-8') as afile:
		qfile.write(latex_preamble_str())
		afile.write(latex_preamble_str())
		for i in range(int(n)):
			(q, a, params) = choose_random_from(list(qtypes.values()))[0](False)
			qstr, astr = latex_question(q, a, params)
			qfile.write(qstr)
			qfile.write('\n')
			afile.write(astr)
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
