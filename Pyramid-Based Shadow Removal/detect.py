import cv2
import numpy as np
cos = np.cos
norm = np.linalg.norm

def dist(v1, v2):
	# Compute the illumination invariant color distance (The cosine similarity)
	return 1 - abs(cos(np.dot(v1, v2)/(norm(v1, ord=2)*norm(v2, ord=2))))

class Shadow_Mask:
	