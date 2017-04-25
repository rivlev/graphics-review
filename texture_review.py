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

qtypes = {
	'l': (linearq, 'linear interpolation'),
}

if __name__ == "__main__":
	rv.main(qtypes)
