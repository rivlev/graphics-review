import numpy
import re
import review as rv
import graphicsFunctions as gf

def magnitudeq(ask=True):
	x = rv.vector3()
	a = gf.magnitude(x)
	q = "||%s||\n" % numpy.array_str(x)
	if ask:
		ua = rv.expect_float(q)
		rv.check_answer(a, 	ua, q, "magnitude")
	else:
		return q, a, ()

def vsumq(ask=True):
	x = rv.vector3()
	y = rv.vector3()
	a = x + y
	q = "%s + %s" % (numpy.array_str(x), numpy.array_str(y))
	if ask:
		ua = rv.expect_vector(q)
		rv.check_answer(a, 	ua, q, "sum")
	else:
		return q, a, ()

def normalizeq(ask=True):
	x = rv.vector3()
	a = gf.normalize(x)
	q = "normalize %s" % numpy.array_str(x)
	if ask:
		ua = rv.expect_vector(q)
		rv.check_answer(a, 	ua, q, "normalize")
	else:
		return q, a, ()

def dot_productq(ask=True):
	x = rv.vector3()
	y = rv.vector3()
	a = x.dot(y)
	q = "%s dot %s\n" % (numpy.array_str(x), numpy.array_str(y))
	if ask:
		ua = rv.expect_float(q)
		rv.check_answer(a, 	ua, q, "dot product")
	else:
		return q, a, ()

def cross_productq(ask=True):
	x = rv.vector3()
	y = rv.vector3()
	a = numpy.cross(x, y)
	q = "%s x %s" % (numpy.array_str(x), numpy.array_str(y))
	if ask:
		ua = rv.expect_vector(q)
		rv.check_answer(a, 	ua, q, "cross_product")
	else:
		return q, a, ()

def directionq(ask=True):
	x = rv.vector3()
	y = rv.vector3()
	a = 'a'
	if (x.dot(y) < 0):
		a = 'b'
	elif x.dot(y) == 0:
		a = 'c'
	q = "What is the relationship between the following two vectors?\n %s, %s\n a) They point in the same direction\n b) they point in opposite directions\n c) they are perpendicular\n" % (numpy.array_str(x), numpy.array_str(y))
	if ask:
		ua = rv.expect_categorical(q, ('a', 'b', 'c'))
		rv.check_answer(a, 	ua, q, "direction")
	else:
		return q, a, ()

def angleq(ask=True):
	x = rv.vector3()
	y = rv.vector3()
	a = numpy.arccos(gf.normalize(x).dot(gf.normalize(y)))
	q = "What is the angle between the following two vectors (in radians)?\n %s, %s\n" % (numpy.array_str(x), numpy.array_str(y))
	if ask:
		ua = rv.expect_float(q)
		rv.check_answer(a, 	ua, q, "angle")
	else:
		return q, a, ()

def point_to_pointq(ask=True):
	x = rv.vector3()
	y = rv.vector3()
	a = y - x
	q = "What is the vector from %s to %s?\n" % (numpy.array_str(x), numpy.array_str(y))
	if ask:
		ua = rv.expect_vector(q)
		rv.check_answer(a, 	ua, q, "point to point")
	else:
		return q, a, ()


qtypes = {
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
	rv.main(qtypes)
