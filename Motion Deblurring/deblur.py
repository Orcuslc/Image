import numpy as np
from psf2otf import psf2otf, isodd
from blur import random_kernel
import cv2

k = 2.7
a = 6.1*1e-4
b = 5.0

# We should regrad the image as a gray-scaled image in the following functions, and combine the result of RGB into one image.

def deblur(img, psf_shape, dim = 1, threshold = 5, lambda1 = 0.1, lambda2 = 20, kappa1 = 1.2, kappa2 = 1.5):
	assert(isodd(psf_shape))
	kernel = random_kernel(psf_shape, np.random.randint(1, psf_shape[0]*psf_shape[1] - 1, dim))	# Initialize the kernel with a randomized estimation
	R, G, B = decompRGB(img)
	(row, col) = R.shape
	omega = smooth_region(R, G, B, psf_shape, threshold)	# Compute the smooth region
	L = img.copy()	# Initialize the L with observed image
	

def single_deblur(I, lambda1, lambda2, omega):
	# Update With a Single Color
	L = I.copy() # Init L with I
	Ix, Iy = np.zeros(I.shape), np.zeros(I.shape)
	Ix[:-1, :], Iy[:, :-1] = I[1:, :] - I[:-1, :], I[:, 1:] - I[:, :-1]
	Ix[-1, :], Iy[:, -1] = Ix[-2, :], Iy[:, -2]
	while True:	# Optimizing L and f
		while True: # Optimizing L
			Lx, Ly = np.zeros(L.shape), np.zeros(L.shape)
			Lx[:-1, :], Ly[:, :-1] = L[1:, :] - L[:-1, :], L[:, 1:] - L[:, :-1]
			Lx[-1, :], Ly[:, -1] = Lx[-2, :], Ly[:, -2]
			ksi_x, ksi_y = update_ksi(Ix, Lx, lambda1, lambda2, gamma), update_ksi(Iy, Ly, lambda1, lambda2, gamma) # update ksi
			

def update_ksi(Iv, Lv, lambda1, lambda2, gamma):
	ksi = np.zeros(Iv.shape)
	k1 = (2*lambda2*omega*Iv + 2*gamma*Lv - lambda1*k)/(2*lambda2*omega + 2*gamma)
	k2 = (2*lambda2*omega*Iv + 2*gamma*Lv + lambda1*k)/(2*lambda2*omega + 2*gamma)
	k3 = (lambda2*omega*Iv + gamma*Lv)/(a*lambda1 + lambda2*omega + gamma)
	E1 = lambda x: lambda1*k*abs(x) + lambda2*omaga*((x - Iv)**2) + gamma*((x - Lv)**2)
	E2 = lambda x: lambda1*k*(a*x**2+b) + lambda2*omaga*((x - Iv)**2) + gamma*((x - Lv)**2)
	E11, E12 = E1(k1), E1(k2)
	E23 = E2(k3)
	E = [[[E11[i, j], E12[i, j], E13[i, j]] for j in range(E11.shape[1])] for i in range(E11.shape[0])]
	argmin = np.argmin(E, axis = 2)
	for i in range(E11.shape[0]):
		for j in range(E11.shape[1]):
			if argmin[i, j] == 0:
				ksi[i, j] = k1[i, j]
			elif argmin[i, j] == 1:
				ksi[i, j] = k2[i, j]
			else:
				ksi[i, j] = k3[i, j]
	return ksi

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