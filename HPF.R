# load in the data from the Cs and Co sources
cs <- data.table::fread("./test_data/Cs.txt")
co <- data.table::fread("./test_data/Co.txt")

# format to matrix
cs_mat <- data.matrix(cs)
co_mat <- data.matrix(co)

# combine matricies
mat <- cs_mat + co_mat

# crop to square matrix
mat_square <- mat[100:500,]
ggplt1 <- display_slice(mat_square)

# apply high-pass filter
fft_slice <- fft(mat_square)
fftshift_slice <- mrbsizeR::fftshift(fft_slice)
scale = 100/(log(1 + max(abs(fft_slice)))) # scaling coefficient (max = 100)
logmagA = scale*log(1 + abs(fftshift_slice)) # scaling
xdim <- ncol(mat_square); ydim <- nrow(mat_square) # dimensions
plane <- pracma::meshgrid(-floor(xdim/2):floor((xdim-1)/2), -floor(ydim/2):floor((ydim-1)/2))
radius <- sqrt(plane$X^2 + plane$Y^2) # circle radius equation

radius_cutoff <- 27
pass <- radius*(radius < radius_cutoff)
F1 <- fftshift_slice * pass # ideal high-pass filter
Fi <- mrbsizeR::ifftshift(F1) # inverse transform to regular
Fi2 <<- abs(fft(Fi, inverse = TRUE))

ggplt2 <- display_slice(Fi2)

display_slice <- function(data){

  part1 <- which(data != "aa", arr.ind = TRUE)
  part2 <- cbind(part1, "V3" = as.numeric(t(data)))
  sl3 <- data.frame(part2)

  fplt <- ggplot(sl3, aes(row, col, z = V3)) +
    geom_raster(aes(fill = V3)) +
    labs(x = "X (pixels)", y = "Y (pixels)") +
    theme(panel.background = element_rect(fill = "white", colour = "grey50")) +
    scale_x_continuous(expand = c(0, 0)) + scale_y_continuous(expand = c(0, 0)) +
    coord_fixed() + scale_fill_gradientn(colours = c("black", "blue", "orange", "white"))
  fplt$labels$fill <- "Nuber of\nOverlaps" # custon legend title
  fplt
}

gridExtra::grid.arrange(ggplt1, ggplt2, nrow = 1)







#
