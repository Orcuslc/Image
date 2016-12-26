from PIL import Image, ImageDraw, ImageDraw2
import random
import numpy as np

class randimage:
	def __init__(self, im):
		self.im2 = im
		self.im = ImageDraw.Draw(im)
		self.size = im.size
		self.x = self.size[0]
		self.y = self.size[1]

	def _rand_xy(self):
		x0 = random.randint(0, self.x - 1)
		x1 = random.randint(0, self.x - 1)
		y0 = random.randint(0, self.y - 1)
		y1 = random.randint(0, self.y - 1)
		return [x0, y0, x1, y1]

	def _rand_angle(self):
		return random.randint(0, 359)

	def _rand_color(self):
		R = random.randint(0, 255)
		G = random.randint(0, 255)
		B = random.randint(0, 255)
		return (R, G, B)

	def _rand_width(self):
		return random.randint(0, 2)

	# def translation(self, )
	def _rectangle