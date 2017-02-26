import review as rv
import numpy
import itertools

def part_of_str_answer_is_in_choices(ua, a):
	ua = ua.lower().strip()
	return any([ua in ax.lower().strip() for ax in a])
	

def ioq():
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
	ua = rv.expect_categorical(q,categories)
	rv.check_answer(a, ua, q, "input/output", part_of_str_answer_is_in_choices)

def cameraq():
	eye = rv.vector3()
	gaze = rv.vector3()
	up = rv.vector3()

	q = "Given a camera position of %s, a gaze vector of %s, and an up vector of %s, what is the resulting camera transformation matrix?" % (numpy.array_str(eye), numpy.array_str(gaze), numpy.array_str(up))

	# derive answer
	w = -rv.normalize(gaze)
	u = rv.normalize(numpy.cross(up, w))
	v = rv.normalize(numpy.cross(w, u))
	a = numpy.matrix([
		[u[0], u[1], u[2], eye[0]],
		[v[0], v[1], v[2], eye[1]],
		[w[0], w[1], w[2], eye[2]],
		[0,		 0,		 0,		 1]
	])

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

qtypes = {
	'io': (ioq, 'input/output'),
	'c': (cameraq, 'camera space'),
}

if __name__ == "__main__":
	rv.main(qtypes)
