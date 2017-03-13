import review as rv
import numpy
import itertools
import graphicsFunctions as gf

def part_of_str_answer_is_in_choices(ua, a):
	ua = ua.lower().strip()
	return any([ua in ax.lower().strip() for ax in a])
	

def ioq(ask=True):
	pipeline = [
		(('object','model'), ('model',), ('world',)),
		(('world',), ('view','camera'), ('camera','eye')),
		(('camera','eye'), ('projection',), ('canonical view volume', 'clip')),
		(('canonical view volume', 'clip'), ('perspective division',), ('2d',)),
		(('2d',), ('viewport',), ('screen',))
	]
	stage = rv.choose_random_from(pipeline)
	space_syn = rv.choose_random_from(("space", "coordinates"))
	qp = (
		rv.choose_random_from(stage[0]),
		rv.choose_random_from(stage[1]),
		rv.choose_random_from(stage[2]),
	)
	qidx = rv.choose_random_from(range(len(qp)))
	q = 'The %s transformation transforms %s %s into %s %s.\n' % (qp[1], qp[0], space_syn, qp[2], space_syn)
	q = q.replace(qp[qidx], rv.blank())

	# hacky: fix phrasing for some terms that don't fit templates
	q = q.replace("The perspective division transformation", "Perspective division")
	q = q.replace("canonical view volume %s" % space_syn, "the canonical view volume")

	a = stage[qidx]
	categories = [y for x in pipeline for y in x[qidx]]
	
	if ask:
		ua = rv.expect_categorical(q,categories)
		rv.check_answer(a, ua, q, "input/output", part_of_str_answer_is_in_choices)
	else:
		return q, a, (categories)

def cameraq(ask=True):
	eye = rv.vector3()
	gaze = rv.vector3()
	up = rv.vector3()

	q = "Given a camera position of %s, a gaze vector of %s, and an up vector of %s, what is the resulting camera transformation matrix?" % (numpy.array_str(eye), numpy.array_str(gaze), numpy.array_str(up))

	# derive answer
	w = -gf.normalize(gaze)
	u = gf.normalize(numpy.cross(up, w))
	v = gf.normalize(numpy.cross(w, u))
	a = numpy.matrix([
		[u[0], u[1], u[2], eye[0]],
		[v[0], v[1], v[2], eye[1]],
		[w[0], w[1], w[2], eye[2]],
		[0,		 0,		 0,		 1]
	])

	if ask:
		ua = rv.expect_matrix(q)

		# nested function for breaking down camera question
		def camera_help(ua, a):
			if rv.lax_equal(a, ua):
				return True;
	
			b = input("Incorrect. Enter 'b' to break down the problem into subproblems, or anything else to abandon this question.\n")	
			if b != 'b':
				return False;
	
			q = "w is the normalized and negated gaze vector. Enter w."
			ua = rv.expect_vector(q)
			rv.check_answer(w, ua, q, "camera.w")
	
			q = "u is the normalized cross product of the up vector and w. Enter u."
			ua = rv.expect_vector(q)
			rv.check_answer(u, ua, q, "camera.u")
	
			q = "v is the normalized cross product of u and w. Enter v."
			ua = rv.expect_vector(q)
			rv.check_answer(v, ua, q, "camera.v")
	
			f = [['ux','uy','uz','px'], ['vx','vy','vz','py'], ['wx','wy','wz','pz'], ['0','0','0','1']]
			print(numpy.array_str(numpy.matrix(f)))
			print(rv.mxstr(f))
	
			q = "The camera transformation matrix is composed of the three basis vectors and camera position in the following order:\n %s\n Enter the camera transformation matrix." % rv.mxstr(f)
			ua = rv.expect_matrix(q)
			return rv.check_answer(a, ua, q, "camera.final")

		rv.check_answer(a, ua, q, "camera", camera_help)

	else:
		return q, a, (eye, gaze, up)

def projectionq(ask=True):
	projectionqs = [
		("Projectors pass through a *viewpoint*.", 'p'),
		("Projectors all are in the same projection *direction*.", 'o'),
		("Further objects are smaller.", 'p'),
		("Parallel lines are preserved.", 'o'),
		("Viewing volume is shaped like a frustum.", 'p'),
		("Viewing volume is shaped like a parallelipiped.", 'o'),
		("Looks more natural.", 'p'),
		("Useful for architectural drawings.", 'o'),
	]

	pq = rv.choose_random_from(projectionqs)
	q = "For which kind of projection is the following statement true? Answer 'p' for perspective or 'o' for orthographic.\n %s " % pq[0]
	a = pq[1]
	if ask:
		ua = rv.expect_categorical(q, ('o', 'p'))
		rv.check_answer(a, ua, q, "projection")
	else:
		return q, a, ()

def perspectiveq(ask=True):
	p = rv.vector3()
	p = numpy.append(p, 1)
	n = rv.vector3()[0]
	if n==0:	
		n = 1

	q = "Project point %s onto the plane n=%d. " % (numpy.array_str(p), n)
	q1 = "What will px, py, pw be after the perspective transformation is applied? (before the scaling and translation of the orthographic transformation) "
	q2 = "What will px, py be after perspective division?"

	a1 = numpy.array((p[0]*n, p[1]*n, p[2]))
	a2 = numpy.array((a1[0]/a1[2], a1[1]/a1[2]))

	if ask:
		print(q)
		ua1 = rv.expect_vector(q1)
		rv.check_answer(a1, ua1, q1, "perspective.a")
		ua2 = rv.expect_vector(q2, 2)
		rv.check_answer(a2, ua2, q2, "perspective.b")
	else:
		finalq = r"%s\\a) %s\\b) %s" % (q, q1, q2)
		finala = r"a) %s \\ b) %s"
		return finalq, finala, ()

def orthomatrix(t, b, r, l, n, f):
	return numpy.matrix([
		[2/(r-l), 0, 0, -(r+l)/(r-l)],
		[0, 2/(t-b), 0, -(t+b)/(t-b)],
		[0, 0, 2/(n-f), -(n+f)/(n-f)],
		[0, 0, 0, 1]
	])

def orthoq(ask=True):
	(t, b, r, l, n, f) = rv.vector(6)
	if t==b:
		t = t+1
	if r==l:
		r = r+1
	if n==f:
		n = n+1
	a = orthomatrix(t, b, r, l, n, f)
	q = "Create a matrix to transform a paralleliped defined by t=%d, b=%d, r=%d, l=%d, n=%d, and f=%d into the canonical view volume (an orthographic projection matrix)." % (t, b, r, l, n, f)
	
	if ask:
		ua = rv.expect_matrix(q)
		rv.check_answer(a, ua, q, "orthographic")
	else:
		return q, a, ()

qtypes = {
	'io': (ioq, 'input/output'),
	'c': (cameraq, 'camera space'),
	'p': (projectionq, 'projection'),
	'pe': (perspectiveq, 'perspective'),
	'o': (orthoq, "orthographic"),
}

if __name__ == "__main__":
	rv.main(qtypes)
