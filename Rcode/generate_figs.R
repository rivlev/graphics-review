setwd("./Rcode")
source("graphicsFunctions.R")

suppressWarnings(library(ggplot2))
library(grid)

sink("r.log")

args <- commandArgs(trailingOnly = TRUE)

print(args)

triangle_orig <- data.frame(x=c(-1, 0, 1), y=c(-1, 1, -1), hj=c(1, 0.5, 0), vj=c(0, 0, 0))
triangle_orig$fill = "blue"

tmx = identity_matrix()
if (args[1] == "rotation") {
	if (args[2] == "x") {
		tmx = rotation_x_matrix(as.numeric(args[3]))
		warning("Rotation around the x-axis will look strange without projection in 2d")
	} else if (args[2] == "y") {
		tmx = rotation_y_matrix(as.numeric(args[3]))
		warning("Rotation around the y-axis will look strange without projection in 2d")
	} else if (args[2] == "z") {
		tmx = rotation_z_matrix(as.numeric(args[3]))
	} else {
		stop(paste("invalid axis; USAGE: rotation AXIS={x,y,z} RADIANS", paste(args, collapse=" "), "args[2]=", args[2]))
	}
} else if (args[1] == "translation") {
	tmx = translation_matrix(as.numeric(args[2]), as.numeric(args[3]), as.numeric(args[4]))
} else if (args[1] == "scale") {
	tmx = scale_matrix(as.numeric(args[2]), as.numeric(args[3]), as.numeric(args[4]))
} else {
	stop(paste("invalid transformation, must be translation, rotation, or scale, not", args[1]))
}

triangle_transformed <- triangle_orig
triangle_transformed[,c("x","y")] <- transform(triangle_transformed[,c("x","y")], tmx)[,c("x","y")]
triangle_transformed$fill = "green"
triangle <- rbind(triangle_orig, triangle_transformed)

p <-
ggplot(triangle, aes(x, y)) +
geom_point() +
geom_polygon(aes(fill=fill), alpha=0.6) +
geom_text(aes(label=paste("(", round(x,2), ",", round(y,2), ")", sep="")), hjust=triangle$hj, vjust=triangle$vj) +
geom_vline(xintercept=0) + geom_hline(yintercept=0) +
xlim(range(triangle$x) + range(triangle$x)/10) + ylim(range(triangle$y) + range(triangle$y)/10) +
scale_fill_brewer(palette = "Set3") +
theme(legend.position="none", axis.title.x = element_blank(), axis.title.y = element_blank(), axis.text.x=element_text(size=18), axis.text.y=element_text(size=18))

# disable text clipping
gt <- ggplot_gtable(ggplot_build(p))
gt$layout$clip[gt$layout$name == "panel"] <- "off"

png("../tmp.png")
grid.draw(gt)
dev.off()

sink()
