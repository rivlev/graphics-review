cross <- function(u, v) {
	c(u[2]*v[3]-u[3]*v[2], u[3]*v[1]-u[1]*v[3], u[1]*v[2]-u[2]*v[1])
}

magnitude <- function(u) {
	res <- 0
	for (i in u) {
		res <- res + i^2
	}
	sqrt(res)
}

normalize <- function(v) {
	v/magnitude(v)
}

dot <- function(u, v) {
	res <- 0
	for (i in 1:length(u)) {
		res <- res + u[i]*v[i]
	}
	res
}

implicitLine <- function(x0, y0, x1, y1, x, y) {
	(y0-y1)*x + (x1-x0)*y + x0*y1 - x1*y0
}

implicitLine <- function(p1, p2, px) {
	(p1[2]-p2[2])*px[1] + (p2[1]-p1[1])*px[2] + p1[1]*p2[2] - p2[1]*p1[2]
}

implicitLineGridSearch <- function(targetf) {
	top <- 5
	for (x0 in sample(0:9)) {
		for (x1 in sample(x0:9)) {
			for (y0 in sample(0:9)) {
				for (y1 in sample(y0:9)) {
					for (x in sample(0:9)) {
						for (y in sample(0:9)) {
							if (implicitLine(x0, y0, x1, y1, x, y)==targetf) return(c(x0, y0, x1, y1, x, y))
	}}}}}}
	"BAD"
}

barycentric <- function(ax, ay, bx, by, cx, cy, px, py) {
  x <- list()
  x[["alpha"]] <- implicitLine(bx, by, cx, cy, px, py) / implicitLine(bx, by, cx, cy, ax, ay)
  x[["beta"]] <- implicitLine(ax, ay, cx, cy, px, py) / implicitLine(ax, ay, cx, cy, bx, by)
  x[["gamma"]] <- implicitLine(ax, ay, bx, by, px, py) / implicitLine(ax, ay, bx, by, cx, cy)
  x
}

barycentric <- function(A, B, C, V) {
	x <- list()
	x[["alpha"]] <- implicitLine(B, C, V)/implicitLine(B, C, A)
	x[["beta"]] <- implicitLine(A, C, V)/implicitLine(A, C, B)
	x[["gamma"]] <- implicitLine(A, B, V)/implicitLine(A, B, C)
	x
}

perp <- function(u) {
  c(-u[2], u[1])
}

implicitPlane <- function(normal, point, testpoint) {
  normal[1]*(testpoint[1]-point[1]) +
  normal[2]*(testpoint[2]-point[2]) +
  normal[3]*(testpoint[3]-point[3])
}

pointOnPlaneGridSearch <- function(normal, point) {
	top <- 5
	for (x in sample(0:9)) {
		for (y in sample(0:9)) {
			for (z in sample(0:9)) {
				if (implicitPlane(normal, point, c(x, y, z))==0) return(c(x, y, z))
	}}}
	"BAD"
}

tOfIntersection <- function(point, normal, p0, p1) {
	dot(point-p0, normal) / dot(p1-p0, normal)
}

# plot data on basic cartesian plot
cart <- function(data) {
	ggplot(data, aes(x, y)) + geom_point() + geom_vline(xintercept=0) + geom_hline(yintercept=0) + xlim(-1, 1) + ylim(-1, 1)
}

identity_matrix <- function() {
	res <- c(1, 0, 0, 0,
		 0, 1, 0, 0,
		 0, 0, 1, 0,
		 0, 0, 0, 1)
	dim(res) <- c(4,4)
	res
}

translation_matrix <- function(xd, yd, zd) {
	res <- c(1, 0, 0, 0,
		 0, 1, 0, 0,
		 0, 0, 1, 0,
		 xd, yd, zd, 1)
	dim(res) <- c(4, 4)
	res
}

rotation_z_matrix <- function(d) {
	res <- c(cos(d), -sin(d), 0, 0,
		 sin(d), cos(d), 0, 0,
		 0, 0, 1, 0,
		 0, 0, 0, 1)
	dim(res) <- c(4, 4)
	res
}

rotation_y_matrix <- function(d) {
	res <- c(cos(d), 0, -sin(d), 0,
		 0, 1, 0, 0,
		 sin(d), 0, cos(d), 0,
		 0, 0, 0, 1)
	dim(res) <- c(4,4)
	res
}

rotation_x_matrix <- function(d) {
	res <- c(1, 0, 0, 0,
		 0, cos(d), -sin(d), 0,
		 0, sin(d), cos(d), 0,
		 0, 0, 0, 1)
	dim(res) <- c(4,4)
	res
}

scale_matrix <- function(sx, sy, sz) {
	res <- c(sx, 0, 0, 0,
		 0, sy, 0, 0,
		 0, 0, sz, 0,
		 0, 0, 0, 1)
	dim(res) <- c(4,4)
	res
}

center_on_origin_matrix <- function(data) {
	minx = min(data$x); maxx <- max(data$x)
	miny = min(data$y); maxy <- max(data$y)
	minz = min(data$z); maxz <- max(data$z)
	dx = -(maxx-minx)/2; dy = -(maxy-miny)/2; dz = -(maxz-minz)/2
	translation_matrix(dx, dy, dz)
}

shear_horizontal_matrix <- function(s) {
	res <- c(1, s, 0, 0,
		 0, 1, 0, 0,
		 0, 0, 1, 0,
		 0, 0, 0, 1)
	dim(res) <- c(4, 4)
	res
}

shear_vertical_matrix <- function(s) {
	res <- c(1, 0, 0, 0,
		 s, 1, 0, 0,
		 0, 0, 1, 0,
		 0, 0, 0, 1)
	dim(res) <- c(4, 4)
	res
}


transform <- function(data, m) {
	res <- data
	if (ncol(res)==2) res$z <- rep(0, nrow(data))
	if (ncol(res)==3) res$w <- rep(1, nrow(data))
	res <- apply(res, 1, function(x) { m %*% as.numeric(x) })
	res <- data.frame(t(res))
	names(res) <- c("x", "y", "z", "w")
	res
}

degrees_to_radians <- function(d) {
	d * pi/180
}

radians_to_degrees <- function(r) {
	r * 180/pi
}

circleFun <- function(center = c(0,0),diameter = 1, npoints = 100){
    r = diameter / 2
    tt <- seq(0,2*pi,length.out = npoints)
    xx <- center[1] + r * cos(tt)
    yy <- center[2] + r * sin(tt)
    return(data.frame(x = xx, y = yy))
}

circleSlice <- function(center=c(0,0), diameter=1, npoints=100, xstart=-0.5, xend=0.5, ystart=-0.5, yend=0.5) {
	c = circleFun(center, diameter, npoints)
	return(c[c$x >= xstart & c$x < xend & c$y >= ystart & c$y < yend,])
}
 
getNormal <- function(a, b, c) {
	u <- b - a
	v <- c - a
	normalize(cross(u, v))
} 


# quiz functions
vtext <- function(v, c=" ") {
	paste(v, collapse=c)
}

