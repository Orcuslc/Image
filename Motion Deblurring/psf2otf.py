# The implementation of the `psf2otf` function in MATLAB using Python
import numpy as np

def isodd(atuple):
	for item in atuple:
		if item % 2 == 0:
			return False
	return True

def psf2otf(psf, shape = None):
	if shape == None:
		shape = psf.shape
	assert(isodd(shape))
	psf = np.roll(np.roll(psf, -int(np.floor(shape[0]/2)), axis = 0), -int(np.floor(shape[1]/2)), axis = 1)
	otf = np.fft.fft2(psf)
	return otf

if __name__ == '__main__':
	l = np.asarray([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
	a = psf2otf(l)
	print(a)