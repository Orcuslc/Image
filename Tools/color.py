import cv2
from numpy import *

def seperate_RGB(img):
	R, G, B = cv2.split(img)
	return R, G, B

def construct_RGB(R, G, B):
	return asarray([[[R[x, y], G[x, y], B[x, y]] for y in range(R.shape[1])] for x in range(R.shape[0])])

if __name__ == '__main__':
	img = cv2.imread('E:\\Chuan\\Pictures\\test.jpg')
	R, G, B = seperate_RGB(img)
	img2 = construct_RGB(R, G, B)
	cv2.imshow('img2', img2)
	k = cv2.waitKey(0)
	if k == 27:
		cv2.destroyAllWindows()