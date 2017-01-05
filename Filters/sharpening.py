# Filters used in sharpening and unsharpening images
from scipy.ndimage import convolve as conv
import cv2
from numpy import *

def laplacian():
	temp = zeros((3, 3))
	temp[0, 1] = temp[1, 0] = temp[1, 2] = temp[2, 1] = -1
	temp[1, 1] = -4
	return temp

