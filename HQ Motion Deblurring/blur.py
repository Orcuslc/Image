# Blur an image; Served as simulation
import cv2
from scipy.ndimage import convolve as conv
import numpy as np

def blur(img, kernel):
	return conv(img, kernel)

def random_kernel(shape, number, dim):
	kernel = np.zeros(shape)
	xmax, ymax = shape[0], shape[1]
	x = np.random.randint(1, xmax - 1)
	y = np.random.randint(1, ymax - 1)
	count = 1
	while count < number:
		kernel[x, y] += 1
		direction = np.random.randint(0, 4)
		if direction == 0 and x > 1:
			x = x - 1
			count += 1
		elif direction == 1 and x < xmax - 1:
			x = x + 1
			count += 1
		elif direction == 2 and y > 1:
			y = y - 1
			count += 1
		elif direction == 3 and y < ymax - 1:
			y = y + 1
			count += 1
	if dim == 3:
		kernel = np.asarray([[[i, i, i] for i in j] for j in kernel])
		return kernel/kernel.sum()
	elif dim == 1:
		return kernel/kernel.sum()


def test(img, shape, number, dim):
	kernel = random_kernel(shape, number, dim)
	blurred = blur(img, kernel)
	kernel[np.where(kernel != 0)] = 255
	return blurred, kernel

if __name__ == '__main__':
	img = cv2.imread('test.jpg')
	blurred, kernel = test(img, shape = (41, 41), number = 1700, dim = 3)
	cv2.imshow('img', blurred)
	cv2.imshow('kernel', kernel)
	k = cv2.waitKey(0)
	if k == 27:
		cv2.destroyAllWindows()