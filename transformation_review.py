import numpy
import review as rv
from PIL import Image
from subprocess import call

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
				ua.append(input().strip().split())
			return numpy.matrix([[float(x) for x in elts] for elts in ua])
		except:
			print("Invalid input.")
		
def mxstr(m):
	"\n".join([" ".join(str(e) for e in elts) for elts in m])
	

def translation_matrix(dx, dy, dz):
	return numpy.matrix([[1, 0, 0, dx], [0, 1, 0, dy], [0, 0, 1, dz], [0, 0, 0, 1]])

def rotation_x_matrix(r):
	return numpy.matrix([
		[1, 0, 0, 0],
		[0, numpy.cos(r), -numpy.sin(r), 0],
		[0, numpy.sin(r), numpy.cos(r), 0],
		[0, 0, 0, 1]
	])

def rotation_y_matrix(r):
	return numpy.matrix([
		[numpy.cos(r), 0, numpy.sin(r), 0],
		[0, 1, 0 , 0],
		[-numpy.sin(r), 0, numpy.cos(r), 0],
		[0, 0, 0, 1]
	])

def rotation_z_matrix(r):
	return numpy.matrix([
		[numpy.cos(r), -numpy.sin(r), 0, 0],
		[numpy.sin(r), numpy.cos(r), 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	])

def rotation_matrix(r, a):
	if a=='x':
		return rotation_x_matrix(r)
	elif a == 'y':
		return rotation_y_matrix(r)
	else:
		return rotation_z_matrix(r)
		
def scale_matrix(sx, sy, sz):
	return numpy.matrix([
		[sx, 0, 0, 0],
		[0, sy, 0, 0],
		[0, 0, sz, 0],
		[0, 0, 0, 1]
	])

def qtext(params):
	if params[0] == "translation":
		return "translate a point %s" % " and ".join("%.0f in the %s direction" % (factor, axis) for axis, factor in sorted(params[1].items()) if factor != 0)
	elif params[0] == "rotation":
		return "rotate a point %.2f radians around the %s-axis" % (params[1], params[2])
	elif params[0] == "scale":
		 return "scale a point %s" % " and ".join(["%.2f along the %s-axis" % (factor, axis) for axis, factor in sorted(params.items()) if factor != 1])
		

def translationq(ask=True, twod=False):
	(x, y, z) = numpy.random.randint(-5, 5, 3)
	if twod:
		z = 0
	q = "Create a matrix to %s." % qtext(("translation", {'x':x, 'y':y, 'z':z}))
	a = translation_matrix(x, y, z)
	if ask:
		ua = expect_matrix(q)
		rv.check_answer(a, ua, q, "translation")
	else:
		return q, a, (x,y,z)

def rotationq(ask=True, twod=False):
	r = numpy.round(numpy.random.random() + numpy.random.random(), 2)
	if twod:
		ax = 'z'
	else:
		ax = numpy.random.permutation(('x','y','z'))[0]
	q = "Create a matrix to %s." % qtext(("rotation", r, ax))
	a = rotation_matrix(r, ax)
	if ask:
		ua = expect_matrix(q)
		rv.check_answer(a, ua, q, "rotation")
	else:
		return q, a, (ax, r)
	
def scaleq(ask=True, twod=False):
	axes = ('x','y','z')
	target_axes = numpy.random.permutation(('x', 'y', 'z'))[:(numpy.random.randint(0, 3)+1)]		# randomly permute (x, y, z), then choose a random slice
	if twod:
		target_axes = [a for a in target_axes if a != 'z']
	params = { a : round(numpy.random.random()*5, 2) if a in target_axes else 1 for a in axes }
	q = "Create a matrix to scale a point %s." % " and ".join(["%.2f along the %s-axis" % (factor, axis) for axis, factor in sorted(params.items()) if axis in target_axes])
	a = scale_matrix(params['x'], params['y'], params['z'])
	if ask:
		ua = expect_matrix(q)
		rv.check_answer(a, ua, q, "scale")
	else:
		return q, a, (params['x'], params['y'], params['z'])

def comboq(ask=True):
	transformations = numpy.random.permutation((translationq, rotationq, scaleq))[:numpy.random.randint(2,4)]
	transformations = [ t(False) for t in transformations ]
	q = "Create a matrix to %s." % ", and then ".join([qt.replace("Create a matrix to ", '')[:-1] for (qt, a, params) in transformations])
	a = numpy.eye(4)
	for q, m, p in reversed(transformations):
		a = a * m
	if ask:
		ua = expect_matrix(q)
		rv.check_answer(a, ua, q, "combo")
	else:
		return q, a, transformations

def pictureq(ask=True):
	transformation = numpy.random.permutation(((translationq, "translation"), (rotationq, "rotation"), (scaleq, "scale")))[0]
	(qt, a, params) = transformation[0](False, True)
	q = "Create a matrix to transform the green triangle into the yellow triangle."
	call(["Rscript", "Rcode/generate_figs.R", transformation[1]] + [str(p) for p in params])
	if ask:
		with Image.open('tmp.png') as img:
			img.show()
			ua = expect_matrix(q)
			rv.check_answer(a, ua, q, "picture")
	else:
		return q, a, params

tqtypes = {
	't': (translationq, 'translation'),
	'r': (rotationq, 'rotation'),
	's': (scaleq, "scale"),
	'c': (comboq, "combo"),
	'p': (pictureq, "picture")
}

if __name__ == "__main__":
	rv.main(tqtypes)
