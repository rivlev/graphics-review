import numpy


def magnitude(v):
	return numpy.sqrt(v.dot(v))

def normalize(v):
	return v / magnitude(v)

def getNormal(vertices):
	return normalize(numpy.cross(vertices[1]-vertices[0], vertices[2]-vertices[0]))

def reflect(v, normal):
	return 2 * normal * (v.dot(normal)) - v
