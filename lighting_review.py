import review as rv
import graphicsFunctions as gf
import numpy

def diffuseColor(cl, cr, ld, normal):
	return cl * cr * max((ld.dot(normal)), 0)

def specularColor(cl, ld, normal, ed, p):
	return cl * max((gf.reflect(ld, normal).dot(ed), 0))**p

def ldirq(ask=True):
	ppos = rv.vector3()
	lpos = rv.vector3()
	q = "Given a point location of %s and a light location of %s, what is the light direction? (Remember to normalize.)" % (numpy.array_str(ppos), numpy.array_str(lpos))
	a = gf.normalize(lpos - ppos)
	if ask:
		ua = rv.expect_vector(q)
		rv.check_answer(a, ua, q, "light direction")
	else:
		return q, a

def normalq(ask=True):
	vertices = [rv.vector3() for _ in xrange(3)]
	q = "What is the normal to a triangle defined by vertices %s, %s, and %s (listed in the order of positive rotation)?" % [numpy.array_str(p) for p in vertices]
	a = gf.getNormal(vertices)
	if ask:
		ua = rv.expect_vector(q)
		rv.check_answer(a, ua, q, "normal")
	else:
		return q, a

def diffuseq(ask=True):
	cl = rv.color()
	cr = rv.color()
	ld = rv.direction()
	normal = rv.direction()
	q = "Point p has a surface color of %s and a surface normal of %s. Given a light of color %s and direction %s, what will be the diffuse component of p's final color?" % (rv.tostring(cr), rv.tostring(normal), rv.tostring(cl), rv.tostring(ld))
	a = cl * cr * max((0, ld.dot(normal)))
	if ask:
		ua = rv.expect_vector(q)
		rv.check_answer(a, ua, q, "diffuse")
	else:
		return q, a

def specularq(ask=True):
	cl = rv.color()
	ld = rv.direction()
	cr = rv.color()
	normal = rv.direction()
	r = gf.reflect(ld, normal)
	e = gf.normalize(rv.vector3())
	p = 2

	q = "Point p has a surface color of %s and a surface normal of %s. Given a light of color %s and direction %s, and a view direction %s, what will be the specular component of p's final color, with a Phong exponent of %d?" % (numpy.array_str(cr), numpy.array_str(normal), numpy.array_str(cl), numpy.array_str(ld), numpy.array_str(e), p)
	a = cl * max((r.dot(e), 0))**p

	if ask:
		ua = rv.expect_vector(q)
		rv.check_answer(a, ua, q, "specular")
	else:
		return q, a

def totalq(ask=True):
	(cr, normal, cl, ld, ed, ca) = (rv.color(), rv.direction(), rv.color(), rv.direction(), rv.direction(), rv.color())
	q = "Point p has a surface color of %s and a surface normal of %s. Given a light of color %s and direction %s, a view direction %s, and an ambient color %s, what will be p's final color, with a Phong exponent of 2?" % tuple(numpy.array_str(s) for s in (cr, normal, cl, ld, ed, ca))

	a = diffuseColor(cl, cr, ld, normal) + specularColor(cl, ld, normal, ed, 2) + ca * cr

	if ask:
		ua = rv.expect_vector(q)
		rv.check_answer(a, ua, q, "total")

qtypes = {
	'l': (ldirq, 'light direction'),
	'n': (normalq, 'normal'),
	'd': (diffuseq, 'diffuse'),
	's': (specularq, 'specular'),
	't': (totalq, 'total color'),
}

if __name__ == "__main__":
	rv.main(qtypes)
