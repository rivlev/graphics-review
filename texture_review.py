#!/usr/bin/python

import review as rv
import graphicsFunctions as gf
import numpy as np

def linearq(ask=True):
	smin, smax, tmin, tmax = rv.vector(4)
	smin, smax = rv.strict_order(smin, smax)
	tmin, tmax = rv.strict_order(tmin, tmax)
	s = np.random.randint(smin, smax+1)
	t = np.random.randint(tmin, tmax+1)

	u = (s-smin)/(smax-smin)
	v = (t-tmin)/(tmax-tmin)

	q = "Given a 2D image texture with coordinates ranging from 0 to 1, and a rectangular surface with x ranging from %d to %d and y ranging from %d to %d, what are the (u, v) texture coordinates of surface point (%d, %d) by simple linear interpolation?" % (smin, smax, tmin, tmax, s, t)

	a = (u, v)

	if ask:
		ua = rv.expect_vector(q, 2)
		rv.check_answer(a, ua, q, 'linear interpolation')
	else:
		return q, a

def bilinearq(ask=True):
	u, v = np.round(np.random.random(2), 2)
	rs, rt = (2**np.random.randint(7, 12) for _ in range(2))
	r1, r2 = np.random.randint(1, 4, 2)
	q = "Given (u, v) coordinates of (%.2f, %.2f) and a texture with resolution %d x %d, where the value at each (s, t) texture location is (s+t+%d)/%d, what is the value retrieved by bilinear interpolation?" % (u, v, rs, rt, r1, r2)

	fn = lambda u, v: (u+v+r1)/r2
	a = gf.bilinearInterpolation(u, v, rs, rt, fn)

	rv.writeModule(dict(zip(("u", "v", "rs", "rt", "a", "fn", "r1", "r2"), (u, v, rs, rt, a, "lambda u, v: (u+v+r1)/r2", r1, r2))))

	if ask:
		ua = rv.expect_float(q)
		rv.check_answer(a, ua, q, 'bilinear interpolation')
	else:
		return q, a

def mipmapq(ask=True):
	ir = np.random.randint(2**4, 2**7)
	q = "Suppose a texture is applied to an area of size %d x %d." % (ir, ir)
	q1 = "What two levels of detail (powers of two) should be used for trilinear interpolation?"
	q2 = "How should each one be weighted?"

	d = np.log2(ir)
	a1 = 2**np.floor(d), 2**np.ceil(d)
	dd = (ir-a1[0])/(a1[1]-a1[0])
	a2 = 1-dd, dd

	rv.writeModule(dict(zip(("ir", "d", "dd", "a1", "a2"), (ir, d, dd, a1, a2))))

	if ask:
		print(q)
		ua1 = rv.expect_vector(q1, 2)
		rv.check_answer(a1, ua1, q1, "level of detail")
		ua2 = rv.expect_vector(q2, 2)
		rv.check_answer(a2, ua2, q2, "trilinear interpolation")
	else:
		return rv.combine((q, q1, q2)), rv.combine((a1, a2), False)

def nearestq(ask=True):	
	u, v = np.round(np.random.random(2), 2)
	rs, rt = np.random.randint(16, 2048, 2)
	q = "Given (u, v) coordinates of (%.2f, %.2f) and a texture of size (%d, %d), what texel will be chosen by nearest neighbor sampling?" % (u, v, rs, rt)

	a = np.round(u*rs), np.round(v*rt)

	rv.writeModule(dict(zip("u,v,rs,rt,a".split(','), (u, v, rs, rt, a))))

	if ask:
		ua = rv.expect_vector(q, 2)
		rv.check_answer(a, ua, q, "nearest neighbor")
	else:
		return q, a

def samplingq(ask=True):
	ir = np.random.randint(2**4, 2**7, 2)
	q1 = "Given a texture of size (%d, %d) and an image of size (%d, %d), how many texels must cover each pixel?" % (ir[0], ir[0], ir[1], ir[1])
	a1 = ir[0]/ir[1]
	q2 = "Is this a problem of magnification (mag) or minification (min)?"
	if ir[0] < ir[1]:
		a2 = "mag"
	else:
		a2 = "min"

	rv.writeModule(dict(zip("ir, a1, a2".split(','), (ir, a1, a2))))

	if ask:
		ua1 = rv.expect_float(q1)
		rv.check_answer(a1, ua1, q1, "texel:pixel")
		ua2 = rv.expect_categorical(q2, ('mag', 'min'))
		rv.check_answer(a2, ua2, q2, "magnification")
	else:
		return rv.combine((q1, q2), False), rv.combine((a1, a2), False)
	
	

qtypes = {
#	'l': (linearq, 'linear interpolation'),
	'b': (bilinearq, 'bilinear interpolation'),
	'm': (mipmapq, 'mipmapping'),
	'n': (nearestq, 'nearest neighbor'),
	's': (samplingq, 'sampling'),
}

if __name__ == "__main__":
	rv.main(qtypes)
