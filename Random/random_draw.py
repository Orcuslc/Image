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

	def _rand_border(self):
		u = int(np.floor(random.random()/0.25))
		if u == 0:
			x0, y0 = 0, random.randint(0, self.y - 1)
		elif u == 1:
			x0, y0 = random.randint(0, self.x - 1), 0
		elif u == 2:
			x0, y0 = self.x - 1, random.randint(0, self.y - 1)
		elif u == 3:
			x0, y0 = random.randint(0, self.x - 1), self.y - 1
		return u, x0, y0

	def _rand_angle(self):
		return random.randint(0, 359)

	def _rand_color(self):
		R = random.randint(0, 255)
		G = random.randint(0, 255)
		B = random.randint(0, 255)
		return (R, G, B)

	def _rand_width(self):
		return random.randint(0, 20)

	def _rand_arc(self):
		self.im.arc(self._rand_xy(), self._rand_angle(), self._rand_angle(), self._rand_color())

	def _rand_chord(self):
		self.im.chord(self._rand_xy(), self._rand_angle(), self._rand_angle(), self._rand_color(), self._rand_color())

	def _rand_line(self):
		self.im.line(self._rand_xy(), self._rand_color(), self._rand_width())

	def _rand_ellipse(self):
		self.im.ellipse(self._rand_xy(), self._rand_color(), self._rand_color())

	def _rand_pieslice(self):
		self.im.pieslice(self._rand_xy(), self._rand_angle(), self._rand_angle(), self._rand_color(), self._rand_color())

	def _rand_point(self):
		self.im.point(self._rand_xy(), self._rand_color())

	def _rand_polygon(self):
		self.im.polygon(self._rand_xy(), self._rand_color(), self._rand_color())

	def _rand_rectangle(self):
		self.im.rectangle(self._rand_xy(), self._rand_color(), self._rand_color())

	def _rand_func(self):
		u = random.random()
		funcs = [self.arc, self.chord, self.line, self.ellipse, self.pieslice, self.point, self.polygon, self.rectangle]
		num = int(np.floor(u/0.125))
		return funcs[num]

	def draw_bones(self, n):
		for i in range(n):
			u0, x0, y0 = self._rand_border()
			while True:
				u1, x1, y1 = self._rand_border()
				if u0 != u1:
					break
			self.im.line([x0, y0, x1, y1], fill = (255, 255, 255), width = 3)

	def _rand_triangle(self, pec):
		u0, x0, y0 = self._rand_border()
		while True:
			u1, x1, y1 = self._rand_border()
			while True:
				u2, x2, y2 = self._rand_border()
				if u2 != u1:
					break
			if u2 != u0 and u1 != u0:
				break
		center_x, center_y = int((x0+x1+x2)/3), int((y0+y1+y2)/3)
		f = lambda x, y: int(y+(y-x)*pec) 
		x0, x1, x2, y0, y1, y2 = f(x0, center_x), f(x1, center_x), f(x2, center_x), f(y0, center_y), f(y1, center_y), f(y2, center_y)
		return [x0, y0, x1, y1, x2, y2]

	def _isout(self, xy):
		t1 = lambda x: 0<=x<=self.x
		t2 = lambda y: 0<=y<=self.y
		r1, r2 = 1-np.asarray([t1(i) for i in xy[::2]]), 1-np.asarray([t2(i) for i in xy[1::2]])
		a1 = 1 if sum(r1) >= 1 else 0
		a2 = 1 if sum(r2) >= 1 else 0
		return (1-a1)*(1-a2)

	def draw_triangle(self, pec, n):
		xy = self._rand_triangle(pec)
		for i in range(n):
			while True:
				dist = [random.randint(int(-self.x/2), int(self.x/2)), random.randint(int(-self.y/2), int(self.y/2))]
				angle = random.random()*2*np.pi
				xy = self._pan(xy, dist)
				xy = self._rotate(xy, angle)
				r = self._isout(xy)
				if r == 1:
					break
			self.im.polygon(xy)


	def _pan(self, xy, dist):
		# return xy
		M = (np.matrix([xy[::2], xy[1::2]]) + np.matrix([[dist[0]], [dist[1]]])).transpose().tolist()
		r = []
		for i in M:
			r += i
		return r

	def _rotate(self, xy, angle):
	# 	[x0, x1, x2], [y0, y1, y2] = xy[::2], xy[1::2]
	# 	center = [(x0+x1+x2)/3, (y0+y1+y2)/3]
	# 	f = lambda x, y: [np.cos(angle)*x - np.sin(angle)*y, np.sin(angle)*x + np.cos(angle)*y]
	# 	g = lambda x, y, center: [center[0]+f(x-center[0], y-center[1])[0], center[1]+f(x-center[0], y-center[1])[1]]
	# 	[x0, y0], [x1, y1], [x2, y2] = g(x0, y0, center), g(x1, y1, center), g(x2, y2, center)
		M = np.matrix([xy[::2], xy[1::2]])
		center = np.mean(M, axis = 1)
		trans = np.matrix([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
		N = (trans * (M - center) + center).transpose().tolist()
		r = []
		for i in N:
			r += i
		return r

	def apply(self, n):
		for i in range(n):
			func = self._rand_func()
			func()

	def show(self):
		del self.im
		self.im2.save('test.jpg')
		self.im2.show()

if __name__ == '__main__':
	size = [277, 277]
	a = Image.new('RGB', size)
	# a.show()
	rim = randimage(a)
	# rim.apply(1000)
	rim.draw_bones(10)
	rim.draw_triangle(0.2, 6)
	rim.show()