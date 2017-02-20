from collections import defaultdict
import numpy
import re
import review

scores = []

def vector3():
	return numpy.random.randint(-5, 5, 3)

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

def check_answer(a, ua, q, qt):
	s = 0
	if lax_equal(ua, a):
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

def magnitudeq():
	x = vector3()
	a = magnitude(x)
	q = "||%s||\n" % numpy.array_str(x)
	ua = expect_float(q)
	check_answer(a, ua, q, "magnitude")

def vsumq():
	x = vector3()
	y = vector3()
	a = x + y
	q = "%s + %s" % (numpy.array_str(x), numpy.array_str(y))
	ua = expect_vector(q)
	check_answer(a, ua, q, "sum")

def normalizeq():
	x = vector3()
	a = normalize(x)
	q = "normalize %s" % numpy.array_str(x)
	ua = expect_vector(q)
	check_answer(a, ua, q, "normalize")

def dot_productq():
	x = vector3()
	y = vector3()
	a = x.dot(y)
	q = "%s dot %s\n" % (numpy.array_str(x), numpy.array_str(y))
	ua = expect_float(q)
	check_answer(a, ua, q, "dot product")

def cross_productq():
	x = vector3()
	y = vector3()
	a = numpy.cross(x, y)
	q = "%s x %s" % (numpy.array_str(x), numpy.array_str(y))
	ua = expect_vector(q)
	check_answer(a, ua, q, "cross_product")

def directionq():
	x = vector3()
	y = vector3()
	a = 'a'
	if (x.dot(y) < 0):
		a = 'b'
	elif x.dot(y) == 0:
		a = 'c'
	q = "What is the relationship between the following two vectors?\n %s, %s\n a) They point in the same direction\n b) they point in opposite directions\n c) they are perpendicular\n" % (numpy.array_str(x), numpy.array_str(y))
	ua = expect_categorical(q, ('a', 'b', 'c'))
	check_answer(a, ua, q, "direction")

def angleq():
	x = vector3()
	y = vector3()
	a = numpy.arccos(normalize(x).dot(normalize(y)))
	q = "What is the angle between the following two vectors (in radians)?\n %s, %s\n" % (numpy.array_str(x), numpy.array_str(y))
	ua = expect_float(q)
	check_answer(a, ua, q, "angle")

def point_to_pointq():
	x = vector3()
	y = vector3()
	a = y - x
	q = "What is the vector from %s to %s?\n" % (numpy.array_str(x), numpy.array_str(y))
	ua = expect_vector(q)
	check_answer(a, ua, q, "point to point")


vqtypes = {
	'r': (directionq, 'direction'), 
	's': (vsumq, 'sum'),
	'm': (magnitudeq, 'magnitude'),
	'n': (normalizeq, 'normalize'),
	'd': (dot_productq, 'dot product'),
	'c': (cross_productq, 'cross product'),
	'a': (angleq, 'angle'),
	'ptp': (point_to_pointq, 'point to point'),
}

def getq(q, qtypes):
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
		q = input("Enter %s, a number n for an n-item quiz, or nothing to quit, and press enter\n" % ", ".join(instructions))
		if q == '':
			report_scores()
			break
		else:
			getq(q, qtypes)

if __name__ == "__main__":
	main(vqtypes)
