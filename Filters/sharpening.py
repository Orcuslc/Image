# Filters used in sharpening and unsharpening images
from scipy.ndimage import convolve as conv
import cv2
from numpy import *

def laplacian(img, order = 3):
	temp = zeros((3, 3))
	temp[0, 1] = temp[1, 0] = temp[1, 2] = temp[2, 1] = -1
	temp[1, 1] = -4
	if order == 3:
		temp = asarray([[[x, x, x] for x in i] for i in temp])
	nimg = img - conv(img, temp)
	return nimg



if __name__ == '__main__':
	img = cv2.imread('../test-images/lion.jpg', 0)	
	nimg = laplacian(img, 1)
	cv2.imshow('img', img)
	cv2.imshow('nimg', nimg)
	k = cv2.waitKey(0)
	if k == 27:
		cv2.destroyAllWindows()