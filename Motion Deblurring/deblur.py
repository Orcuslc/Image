import numpy as np
from psf2otf import psf2otf, isodd
from blur import random_kernel
import cv2

# We should regrad the image as a gray-scaled image in the following functions, and combine the result of RGB into one image.

def deblur(img, psf_shape, dim = 1):
	assert(isodd(psf_shape))
	kernel = random_kernel(psf_shape, np.random.randint(1, psf_shape[0]*psf_shape[1] - 1, dim))

def decompRGB(img):
	R = np.asarray([[i[0] for i in j] for j in img])
	G = np.asarray([[i[1] for i in j] for j in img])
	B = np.asarray([[i[2] for i in j] for j in img])
	return R, G, B

def single_smooth_region(img, psf_shape, threshold = 5):
	(row, col) = img.shape
	hprow, hpcol = tuple(map(lambda x: int(np.floor(x/2)), psf_shape))
	window = np.zeros(img.shape)
	for x in range(row):
		for y in range(col):
			local_window = img[max(0, x - hprow):min(row, x + hprow), max(0, y - hpcol):min(col, y + hpcol)]
			t = np.std(local_window)
			if t < threshold:
				window[x, y] = 1
	return window

def smooth_region(R, G, B, psf_shape, threshold = 5):
	Rwindow = single_smooth_region(R, psf_shape, threshold)
	Gwindow = single_smooth_region(G, psf_shape, threshold)
	Bwindow = single_smooth_region(B, psf_shape, threshold)
	window = Rwindow * Gwindow * Bwindow
	window[np.where(window == 1)] = 255
	return window

if __name__ == '__main__':
	img = cv2.imread('test_blurred.jpg')
	R, G, B = decompRGB(img)
	Rwindow = smooth_region(R, G, B, (27, 27), 3)
	cv2.imshow('RWindow', Rwindow)
	k = cv2.waitKey(0)
	if k == 27:
		cv2.destroyAllWindows()