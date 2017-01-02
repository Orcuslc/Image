import cv2
import numpy as np
from scipy.ndimage import convolve as conv
cos = np.cos
norm = np.linalg.norm
pi = np.pi
exp = np.exp

def dist(v1, v2):
	# Compute the illumination invariant color distance (The cosine similarity)
	return 1 - abs(cos(np.dot(v1, v2)/(norm(v1, ord=2)*norm(v2, ord=2))))

def gaussian_average(img, shape = (5, 5), sigma = 1):
	# Gaussian Average Operator
	gaussian_template = np.zeros(shape)
	for i in range(shape[0]):
		for j in range(shape[1]):
			gaussian_template[i, j] = 1/(2*pi*sigma**2)*exp(-((i+1)**2+(j+1)**2)/(2*sigma**2))
	return conv(img, gaussian_template)

def canny_border(img):
	# Detect Borders with Canny Border Detection


class Shadow_Mask:
	