import numpy.random
import codecs

scores = []

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
		q = input("Enter %s, a number n for an n-item quiz, 'review' to save a pdf quiz, or nothing to quit, and press enter " % ", ".join(instructions))
		if q == '':
#			report_scores()
			break
		else:
			getq(q, qtypes)
