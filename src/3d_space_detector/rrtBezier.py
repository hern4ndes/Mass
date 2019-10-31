import random
import pygame
import numpy as np

from pygame.locals import *
from scipy.special import binom
from math import sqrt,cos,sin,atan2

class bezier():
	def __init__(self, xdim, ydim):
		self.XDIM = xdim
		self.YDIM = ydim
		self.EPSILON = 20
		self.NUMNODES = 100  # 500

	def bernstein_poly(self, i, n, t):
	    coeff = binom(n, i)

	    return coeff * t**i * (1 - t)**(n - i)

	def bezier_curve(self, points, nTimes=1000):
	
		nPoints = len(points)
		xPoints = np.array([p[0] for p in points])
		yPoints = np.array([p[1] for p in points])

		t = np.linspace(0.0, 1.0, nTimes)

		polynomial_array = np.array([self.bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)])

		xvals = np.dot(xPoints, polynomial_array)
		yvals = np.dot(yPoints, polynomial_array)

		return xvals, yvals
		#ta dando pau aqui	

	def dist(self, p1, p2):
		try:
			return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))
		except:
			return 0
			#aqui tbm tá dando pau

	def step_from_to(self, p1, p2):
		if self.dist(p1,p2) < self.EPSILON:
			return p2
		else:
			theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
			return p1[0] + self.EPSILON*cos(theta), p1[1] + self.EPSILON*sin(theta)

	def point_circle_collision(self, p1, obstacles, radius):
		for p2 in obstacles:
			distance = self.dist(p1, p2)
			if (distance < radius):
				return True
		return False

	def main(self, obstacles, init_point, end_point):
		if init_point and end_point:
			nodes = []
			nodes.append(init_point)
			reach = False

			while not reach:
				best_node = None
				base_node = nodes[-1]

				for i in range(self.NUMNODES):
					x_i = 1
					x_f = int(self.XDIM)
					y_i = 1
					y_f = int(self.YDIM)
					rand_node = [random.randint(x_i, x_f), random.randint(y_i, y_f)]
					while rand_node == None:
						rand_node = [random.randint(x_i, x_f), random.randint(y_i, y_f)]

					if best_node == None or (self.dist(rand_node, end_point) < self.dist(best_node, end_point)):
						# esse ponto não serve pq depois de calcular o step from to ele é ruim
						rand_node = self.step_from_to(base_node, rand_node)
						# print(base_node)
						if self.point_circle_collision(rand_node, obstacles, 30) == False:
							best_node = rand_node

				newnode = self.step_from_to(base_node, best_node)
				nodes.append(newnode)

				if self.dist(newnode, end_point) < self.EPSILON:
					reach = True
					init_point = None
					end_point = None

		# Suavização de bezier
		suav = []

		xvals, yvals = self.bezier_curve(nodes, nTimes = 100)

		for p in range(len(xvals)):
			suav.append([int(xvals[p]), int(yvals[p])])

		return suav