import review as rv
import graphicsFunctions as gf

import numpy

def triangleq(ask=True):
	p, n = gf.plane()
	vertices = gf.polygon(p, n, 3)
	if rv.coinflip(0.5):
		px = gf.pointProbablyInPolygon(vertices)
	else:
		px = gf.pointNotInPolygon(vertices)

	e, d = gf.rayToPoint(px)

	q = "Triangle T has vertices p0=%s, p1=%s, p2=%s. Ray R has starting point e=%s and direction d=%s." % tuple(numpy.array_str(s) for s in tuple(vertices) + (e, d))

	q1 = "What are the β and 𝛾 barycentric coordinates and the t distance along the ray of the intersection between R and the plane defined by T?"

	# answer calculations
	e1 = vertices[1]-vertices[0]
	e2 = vertices[2]-vertices[0]
	x = numpy.cross(d, e2)
	m = e1.dot(x)		# determinant of original matrix
	s = e - vertices[0] # solution
	beta = s.dot(x)/m		# |-d s p2-p0| = -(-d x (p2-p0)) dot s
	r = numpy.cross(s, e1)
	gamma = d.dot(r)/m
	t = e2.dot(r)/m
	a1 = (beta, gamma, t)

	q2 = "Is the intersection point inside the triangle?"
	a2 = beta >= 0 and beta <= 1 and gamma >= 0 and gamma <= 1

	q3 = "Is the intersection point in front of the viewpoint e?"
	a3 = t > 0

	rv.writeModule(dict(zip(('p','n','vertices','e','d','e1','e2','x','m','s','beta','r','gamma','t', 'px'), (p, n, vertices, e, d, e1, e2, x, m, s, beta, r, gamma, t, px))))

	if ask:
		print(q)
		ua = rv.expect_vector(q1)
		rv.check_answer(numpy.array(a1), ua, q1, "triangle intersection", rv.vector_check)
		ua = rv.expect_boolish(q2, {'y':True, 'n':False} )
		rv.check_answer(a2, ua, q2, "triangle inside", rv.bool_check)
		ua = rv.expect_boolish(q3, {'y':True, 'n':False} )
		rv.check_answer(a3, ua, q3, "ray distance", rv.bool_check)
	else:
		finalq = r"%s\\a) %s\\b) %s\\c) %s" % (q, q1, q2, q3)
		finala = r"a) %s \\b) %s \\c) %s" % (numpy.array_str(a1), a2, a3)
		return finalq, finala, ()

def polygonq(ask=True):
	p, n = gf.plane()
	vertices = gf.polygon(p, n)
	if rv.coinflip(0.5):
		px = gf.pointProbablyInPolygon(vertices)
	else:
		px = gf.pointNotInPolygon(vertices)
	e, d = gf.rayToPoint(px)

	q = "Ray R has starting point e=%s and direction d=%s.\n Polygon P has vertices \n%s." % (numpy.array_str(e), numpy.array_str(d), '\n'.join(numpy.array_str(v) for v in vertices))
	print(q)

	q1 = "What is the normal to P?"
	a1 = gf.getNormal(vertices)
	
	q2 = "What is the t intersection point of R and P?"
	a2 = gf.rayPlane(e, d, v=vertices)

	q3 = "What is the (x, y, z) intersection point on R at t?"
	a3 = gf.pointOnRay(e, d, a2)

	q4 = "Is the intersection point inside the polygon?"
	a4 = gf.pointInPolygon(a3, vertices)

	q5 = "Is the intersection point in front of the viewpoint e?"
	a5 = a2 > 0

	if ask:
		ua1 = rv.expect_vector(q1)
		rv.check_answer(a1, ua1, q1, "normal", rv.vector_check)
		ua2 = rv.expect_float(q2)
		rv.check_answer(a2, ua2, q2, "ray-plane", rv.float_check)
		ua3 = rv.expect_vector(q3)
		rv.check_answer(a3, ua3, q3, "point on ray", rv.vector_check)
		ua4 = rv.expect_yesno(q4)
		rv.check_answer(a4, ua4, q4, "point in polygon", rv.bool_check)
		ua5 = rv.expect_yesno(q5)
		rv.check_answer(a5, ua5, q5, "ray distance", rv.bool_check)
	else:
		return rv.combine((q, q1, q2, q3, q4, q5)), rv.combine((a1, a2, a3, a4,a5), False), ()

def lineq(ask=True):
	p0 = rv.vector3()
	p1 = rv.vector3()
	q = "What are the A, B, and C components of the line passing through %s and %s, where Ax + By + C = 0" % (numpy.array_str(p0), numpy.array_str(p1))
	a = gf.lineEq(p0, p1)[:-1]
	rv.writeModule(dict(zip(('p0','p1','a'), (p0, p1,a))))
	if ask:
		ua = rv.expect_vector(q)
		rv.check_answer(a, ua, q, "line equation", rv.vector_check)
	else:
		return q, a, ()

def barycentricq(ask=True):
	triangle = gf.triangle()
	if rv.coinflip(.5):
		p = gf.pointProbablyInPolygon(triangle)
	else:
		p = gf.pointNotInPolygon(triangle)
	bary = gf.getBarycentricCoordinates(triangle, p)
	
	q1 = "What are the barycentric coordinates of point P=%s with respect to triangle T with vertices\n %s?" % (numpy.array_str(p), '\n'.join(' '.join("%.2f" % v for v in vx) for vx in triangle))
	a1 = bary

	q2 = "Is point P inside or outside T?"
	a2 = (bary >= 0).all() and (bary <= 1).all()

	colors = numpy.array([rv.color() for _ in range(3)])
	q3 = "If vertex 0 has color %s, and vertex 1 has color %s, and vertex 2 has color %s, what is P's color?" % tuple(numpy.array_str(c) for c in colors)
	a3 = sum(b*c for b,c in zip(bary, colors))

	rv.writeModule(dict(zip(('triangle','p','bary','colors','a1','a2','a3'), (triangle, p, bary, colors, a1, a2, a3))))

	if ask:
		ua1 = rv.expect_vector(q1)
		rv.check_answer(a1, ua1, q1, "barycentric coordinates", rv.vector_check)
		ua2 = rv.expect_boolish(q2, {'inside':True, 'outside':False} )
		rv.check_answer(a2, ua2, q2, "barycentric inside", rv.bool_check)
		if a2:
			ua3 = rv.expect_vector(q3)
			rv.check_answer(a3, ua3, q3, "barycentric mixing", rv.vector_check)
	else:
		return rv.combine(q1, q2, q3), rv.combine(a1, a2, a3), ()

def rayq(ask=True):
	# camera frame
	x = gf.normalize(rv.vector3())
	y = gf.normalize(rv.vector3())
	z = gf.normalize(rv.vector3())
	e = rv.vector3()

	# view volume
	l, r, b, t = numpy.random.randint(-5, 5, 4)

	# u, v, coordinates
	i, j = numpy.random.randint(0, 5, 2)
	nx, ny = numpy.random.randint(250, 750, 2)
	u = l + (r-l)*(i+0.5)/nx
	v = b + (t-b)*(j+0.5)/ny

	# ray	
	if rv.coinflip(0.5):
		vt = 'orthographic'
		d = -z
		o = e + u*x + v*y
		ip = None
	else:
		vt = 'perspective'
		ip = numpy.random.randint(0, 5)
		o = e
		d = -ip*z + u*x + v*y

	q = """What are the origin and direction of a ray cast from the viewpoint to pixel (%d, %d) in a %d x %d image with the following parameters?
	l=%d, r=%d, b=%d, t=%d
	view type = %s
	camera origin = %s
	camera u axis = %s
	camera v axis = %s
	camera w axis = %s
	""" % (i, j, nx, ny, l, r, b, t, vt, numpy.array_str(e), numpy.array_str(x), numpy.array_str(y), numpy.array_str(z))
	if v == 'perspective':
		q = q + "image plane at distance %d in front of viewpoint\n" % ip

	rv.writeModule(dict(zip(('i', 'j', 'nx', 'ny', 'l', 'r', 'b', 't', 'vt', 'e', 'x', 'y', 'z', 'ip', 'u', 'v', 'o', 'd'), (i, j, nx, ny, l, r, b, t, vt, e, x, y, z, ip, u, v, o, d)))) 

	if ask:
		print(q)
		ua = rv.expect_vector("origin:")
		rv.check_answer(ua, o, rv.vector_check, "ray casting: origin")
		ua = rv.expect_vector("direction:")
		rv.check_answer(ua, d, rv.vector_check, "ray casting: direction")
	else:
		return q, (o, d), ()


qtypes = {
	'b':	(barycentricq, 'barycentric'),
	't':	(triangleq, 'triangle intersection'),
	'p':	(polygonq, 'polygon intersection'),
	'l':	(lineq, 'line equation'),
	'r':	(rayq, 'ray casting'),
#	's':	(sphereq, 'sphere intersection')
}

if __name__ == "__main__":
	rv.main(qtypes)
