import numpy
import review as rv

def magnitude(v):
	return numpy.sqrt(v.dot(v))

def normalize(v):
	return v / magnitude(v)

def getNormal(vertices):
	return normalize(numpy.cross(vertices[1]-vertices[0], vertices[2]-vertices[0]))

def reflect(v, normal):
	return 2 * normal * (v.dot(normal)) - v

def rayPlane(e, d, n=None, p=None, v=None):
	if n is None:
		n = getNormal(v)
	if p is None:
		p = v[0]
	print(p-e)
	print((p-e).dot(n))
	print(d.dot(n))
	print((p-e).dot(n)/d.dot(n))
	return (p-e).dot(n)/d.dot(n)

def pointOnRay(e, d, t):
	return e + t*d

def lineEq(p0, p1):	# todo remove z coordinate
	A = p0[1]-p1[1]
	B = p1[0]-p0[0]
	C = p0[0]*p1[1] - p1[0]*p0[1]
	return numpy.array((A, B, C)), lambda p : A*p[0] + B*p[1] + C

def xIntersect(v0, v1, y):
	(A, B, C), f = lineEq(v0, v1)
	return (-B*y-C)/A

def getBarycentricCoordinates(triangle, p):
	coef, fab = lineEq(triangle[0], triangle[1])
	coef, fac = lineEq(triangle[0], triangle[2])
	beta = fac(p)/fac(triangle[1])
	gamma = fab(p)/fab(triangle[2])
	return numpy.array((1-beta-gamma, beta, gamma))

def pointInPolygon(p, vertices):
	inside = False
	e0 = vertices[-1]
	y0 = e0[1] >= p[1]
	i = 0
	for e1 in vertices:
		print(i)
		print("Previous vertex above py: %r" % y0)
		y1 = e1[1] >= p[1]
		print("Current vertex above py: %r" % y1)
		if y0 != y1:
			if e0[0] > p[0] and e1[0]> p[0]:
				inside = not inside
				print("both on right: flipping inside to %r" % inside)
			elif e0[0] < p[0] and e1[0] < p[0]:
				print("both on left: skipping")
				continue
			else:
				print("checking x intersection")
				if xIntersect(e0, e1, p[1]) > p[0]:
					inside = not inside
					print("x intersection is on right of px: flipping inside to %r" % inside)
		e0 = e1
		y0 = y1
		i = i+1
	return inside

def pointOnPlane(p, n):
	# find point whose vector to p is perpendicular to n
	# take another random vector and take the cross product of that and n
	# now we have a vector perpendicular to n
	# add that to p to get another point on the plane.
	v = rv.vector3()
	v2 = numpy.cross(v, n)
	p2 = p + v2
	if not (p-p2).dot(n) < 0.000001:
		print("ERROR")
		return (v, v2, p2)
	return p2

def polygon(p, n, nv=5):
	vertices = [pointOnPlane(p, n) for _ in range(nv)]
	for i in range(1, len(vertices)-1):
		if (getNormal(vertices[i-1:]) != n).any():
			vertices[i], vertices[i+1] = vertices[i+1], vertices[i]
	return vertices

def triangle():
	return [rv.vector3() for _ in range(3)]

def plane():
	return rv.vector3(), normalize(rv.vector3())

def ray():
	return rv.vector3(), normalize(rv.vector3())

def rayToPoint(p):
	d = numpy.random.random() * rv.vector3()
	e = p + d
	return e, -normalize(d)

def angle(v1, v2):
	return numpy.arccos(v1.dot(v2)/(magnitude(v1)*magnitude(v2)))

def goodBarycentric():
	bary = numpy.array([numpy.random.random() for _ in range(3)])
	while (bary < 0).any() or sum(bary)!=1:
		a = numpy.random.random()
		b = numpy.random.random()
		bary = numpy.array((0, 0, 1)) + a*numpy.array((1, 0, -1)) + b*numpy.array((0, 1, -1))
	return bary

def pointProbablyInPolygon(vertices):
	# treat first three vertices as triangle and return point in that
	# triangle. Not necessarily in polygon if it is concave or complex
	(alpha, beta, gamma) = goodBarycentric()
	return alpha*vertices[0] + beta*vertices[1] + gamma*vertices[2]

def pointNotInPolygon(vertices):
	# return point with x less than min x of vertices but y in that range
	# so that will have some intersections
	x = min(v[0] for v in vertices) - numpy.random.random()*10
	ys = [v[1] for v in vertices]
	y = min(ys) + numpy.random.random()*(max(ys)-min(ys))
	return numpy.array((x,y,1))

def numberInRange(l, h):
	return numpy.random.randint(l+0.1, h)

def numberNotInRange(l, h):
	x = numpy.random.randint(-5, 5)
	if rv.coinflip(0.5):
		return l-x
	else:
		return h+x

def pointInBox(xmin, ymin, zmin, xmax, ymax, zmax):
	return numpy.array(numberInRange(n, x) for n, x in zip((xmin, ymin, zmin), (xmax, ymax, zmax)))

def pointNotInBox(xmin, ymin, zmin, xmax, ymax, zmax):
	return numpy.array(numberInRange(n, x) if rv.coinflip(0.5) else numberNotInRange(n, x) for n, x in zip((xmin, ymin, zmin), (xmax, ymax, zmax)))

def linearInterpolation(umin, umax, smin, smax, s):
	return umin + (s-smin)/(smax-smin) * (umax - umin)

def bilinearInterpolation(u, v, rs, rt, fn):
	pu, pv = u*rs, v*rt
	wu, wv = (p-numpy.floor(p) for p in (pu, pv))
	return (1-wu) * (1-wv) * fn(numpy.floor(pu), numpy.floor(pv)) + (1-wu) * wv * fn(numpy.floor(pu), numpy.ceil(pv)) + wu * (1-wv) * fn(numpy.ceil(pu), numpy.floor(pv)) + wu * wv * fn(numpy.ceil(pu), numpy.ceil(pv))
