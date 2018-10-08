import numpy as np
import math
import random


# All indices start at 0 #
class Tile:
	# Data  is the data matrix : Type = list of numpy arrays
	# Doc entity model  :shape [ i, j , k]
	# i = Number of entity domains
	# j = number of documents
	# k = number of elements in entity k
	# For doc-entity model
	# domain_idx1 = 0
	# domain_idx2 = [index(s) of j]
	# Entity-Entity model
	# shape = [i, j, k]
	# i = index of binary relation
	# j rows of ith binary relation
	# k columns of ith binary relation

	def __init__(self, domain_idx1, domain_idx2, Data):
		self.ed1 = domain_idx1
		self.ed2 = domain_idx2
		self.r_t = { }
		self.c_t = { }
		self.lambda_m = random.random()
		self.lambda_v = None
		self.data = Data
		return

	# Input is ed, list of rows, list of columns
	def set_elements(self, ed, r_t, c_t):
		if ed not in self.ed2:
			print('ERROR in entity domain reference')
			exit(1)
		self.r_t[ed] = r_t
		self.c_t[ed] = c_t
		print(self.r_t, self.c_t)

	def get_f_m(self):
		s = 0.0
		for _ed2 in self.ed2:
			for i in self.r_t[_ed2]:
				for j in self.c_t[_ed2]:
					s += self.data[_ed2][i][j]
		return s

	def get_f_v(self):
		s = 0.0
		for _ed2 in self.ed2:
			for i in self.r_t[_ed2]:
				for j in self.c_t[_ed2]:
					s += math.pow(self.data[_ed2][i][j], 2)
		return s

	def check(self, ed, i, j):
		if (ed in self.ed2) and (i in self.r_t[ed]) and (j in self.c_t[ed]):
			return True
		return False

	def check_and_get_lambda_m(self, ed, i, j):
		if self.check(ed, i, j):
			return self.lambda_m
		return 0

	def check_and_get_lambda_v(self, ed, i, j):
		if self.check(ed, i, j):
			return self.lambda_v
		return 0




# Data = [np.random.random([3, 5]), np.random.random([3, 4]), np.random.random([3, 6])]
# print(Data)
# t = Tile(0, [2], Data)
# t.set_elements(2, [0, 2], [0, 1, 4])
# print(t.check_and_get_lambda_m(2, 2, 1))
# print(t.get_f_v())
