# Templates for filters
import cv2
from numpy import *


def laplacian(order = 3):
	return asarray([[1, 1, 1],
					[1, -8, 1],
					[1, 1, 1]])

