import cv2
from numpy import *
import os

def resample(img, percentile):
	return img[::(1/percentile), ::(1/percentile)]

def resample_dir(dir1, dir2, percentile = 0.3):
	for file in os.listdir(dir1):
		img = cv2.imread(dir1+file)
		img2 = resample(img, percentile)
		cv2.imwrite(dir2+file.split('.')[0]+'.jpg', img2)

if __name__ == '__main__':
	# img = cv2.imread('E:\\Desktop\\test.jpg')
	# img2 = resample(img, percentile = 0.3)
	# # cv2.imshow('img2', img)
	# cv2.imwrite('E:\\Desktop\\test2.jpg', img2)
	# k = cv2.waitKey(0)
	# if k == 27:
	# 	cv2.destroyAllWindows()
	resample_dir(dir1 = 'E:\\Desktop\\pic\\', dir2 = 'E:\\Desktop\\pic2\\')