import numpy
import re
import review as rv

def magnitudeq():
	x = rv.vector3()
	a = gf.magnitude(x)
	q = "||%s||\n" % numpy.array_str(x)
	ua = rv.expect_float(q)
	rv.check_answer(a, ua, q, "magnitude")

def vsumq():
	x = rv.vector3()
	y = rv.vector3()
	a = x + y
	q = "%s + %s" % (numpy.array_str(x), numpy.array_str(y))
	ua = rv.expect_vector(q)
	rv.check_answer(a, ua, q, "sum")

def normalizeq():
	x = rv.vector3()
	a = gf.normalize(x)
	q = "normalize %s" % numpy.array_str(x)
	ua = rv.expect_vector(q)
	rv.check_answer(a, ua, q, "normalize")

def dot_productq():
	x = rv.vector3()
	y = rv.vector3()
	a = x.dot(y)
	q = "%s dot %s\n" % (numpy.array_str(x), numpy.array_str(y))
	ua = rv.expect_float(q)
	rv.check_answer(a, ua, q, "dot product")

def cross_productq():
	x = rv.vector3()
	y = rv.vector3()
	a = numpy.cross(x, y)
	q = "%s x %s" % (numpy.array_str(x), numpy.array_str(y))
	ua = rv.expect_vector(q)
	rv.check_answer(a, ua, q, "cross_product")

def directionq():
	x = rv.vector3()
	y = rv.vector3()
	a = 'a'
	if (x.dot(y) < 0):
		a = 'b'
	elif x.dot(y) == 0:
		a = 'c'
	q = "What is the relationship between the following two vectors?\n %s, %s\n a) They point in the same direction\n b) they point in opposite directions\n c) they are perpendicular\n" % (numpy.array_str(x), numpy.array_str(y))
	ua = rv.expect_categorical(q, ('a', 'b', 'c'))
	rv.check_answer(a, ua, q, "direction")

def angleq():
	x = rv.vector3()
	y = rv.vector3()
	a = numpy.arccos(gf.normalize(x).dot(gf.normalize(y)))
	q = "What is the angle between the following two vectors (in radians)?\n %s, %s\n" % (numpy.array_str(x), numpy.array_str(y))
	ua = rv.expect_float(q)
	rv.check_answer(a, ua, q, "angle")

def point_to_pointq():
	x = rv.vector3()
	y = rv.vector3()
	a = y - x
	q = "What is the vector from %s to %s?\n" % (numpy.array_str(x), numpy.array_str(y))
	ua = rv.expect_vector(q)
	rv.check_answer(a, ua, q, "point to point")


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

if __name__ == "__main__":
	rv.main(vqtypes)
