import numpy as np
import scipy as sp
from copy import deepcopy

def get_size(img):
	return list(img.shape)[:2]

def get_dist(x0, x1):
	return (abs(x0 - x1) ** 2).sum()

def Gauss_Seidel(A, b, error = 1e-8, max_iter = 1000):
	n, m = get_size(A)
	x0 = np.zeros(n) + 0.5
	for k in range(max_iter):
		x1 = deepcopy(x0)
		for i in range(n):
			x0[i] = (1/A[i, i]) * (b[i] - np.dot(A[i, :], x1) + A[i, i] * x1[i])
		dist = get_dist(x0, x1)
		if dist < error:
			return x0
	return x1

class discrete_poisson_solver:
	''' Solver of discrete Poisson Equation with Dirichlet boundary conditions
		v: The guidance field, expressed with a Matrix;
		img: The original image, providing boundary conditions;
		mask: The mask pointing out the region omega, where v is defined in; elements in 
			the mask are -1(outside omega), 0(on the border of omega), 1(inside omega)
	'''
	def __init__(self, v, img, mask):
		self.v = v
		self.mask = mask
		self.img = img # The f* in the paper;
		self.row, self.col = get_size(img)
		self.size = self.row * self.col
		self.A = np.zeros((self.size, self.size)) # The coeff. matrix of discrete Poisson Equations;
		self.b = np.zeros((self.size, 3)) # The constance vector of discrete Poisson Equations;

	def make_equations(self):
		for i in range(self.row):
			for j in range(self.col):
				index = i * col + j # The index of f;
				if self.mask[i, j] == 1: # The pixel p is in omega;
					self.A[index, index] = self._calc_np_size(i, j) # For p in Omega;
					if self._is_in_np_omega(x, y - 1): # The left pixel of p;
						self.A[index, index - 1] = -1
					if self._is_in_np_omega(x, y + 1): # The right pixel of p;
						self.A[index, index + 1] = -1
					if self._is_in_np_omega(x - 1, y): # The upper pixel of p;
						self.A[index, index - self.col] = -1
					if self._is_in_np_omega(x + 1, y): # The lower pixel of p;
						self.A[index, index + self.col] = -1
					
					if self._is_in_np_omega_boundary(x, y - 1): 
						self.b[index] += self.img[x, y - 1]
					if self._is_in_np_omega_boundary(x, y + 1):
						self.b[index] += self.img[x, y + 1]
					if self._is_in_np_omega_boundary(x - 1, y):
						self.b[index] += self.img[x - 1, y]
					if self._is_in_np_omega_boundary(x + 1, y):
						self.b[index] += self.img[x + 1, y]

					self.b[index] += sum(self.v[i, j])


	def _is_in_np_omega(self, x, y):
		if (x < 0 or x >= self.row) or (y < 0 or y >= self.col):
			return False
		else:
			if self.mask[x, y] == 1: # is in omega;
				return True
			else:
				return False

	def _is_in_np_omega_boundary(self, x, y):
		if (x < 0 or x >= self.row) or (y < 0 or y >= self.col):
			return False
		else:
			if self.mask[x, y] == 0: # is on the boundary;
				return True
			else:
				return False

	def _calc_np_size(self, x, y):
		if x == 0 or x == self.row - 1:
			if y == 0 or y == self.col - 1:
				return 2
			else:
				return 3
		else:
			if y == 0 or y == self.row - 1:
				return 3
			else:
				return 4

	def _calc_np_boundary_size(self, x, y):
		left = (x, y - 1)
		right = (x, y + 1)
		up = (x - 1, y)
		down = (x + 1, y)

	def solve(self):
		r = Gauss_Seidel(self.A, self.b[:, 0])
		g = Gauss_Seidel(self.A, self.b[:, 1])
		b = Gauss_Seidel(self.A, self.b[:, 2])
		self.Nimg = np.zeros((self.row, self.col, 3), dtype = np.uint8)
		for i in range(self.row):
			for j in range(self.col):
				index = i * self.col + j
				if max(abs(self.A[index, :])) == 0:
					self.Nimg[i, j] = self.img[i, j]
				else:
					self.Nimg[i, j] = np.asarray([r[index], g[index], b[index]], dtype = np.uint8)
		return self.Nimg


if __name__ == '__main__':
	A = np.array([[1, 1], [2, 3]])
	b = np.array([[2], [3]])
	x1 = Gauss_Seidel(A, b)
	print(x1)