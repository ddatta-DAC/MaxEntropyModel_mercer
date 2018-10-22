import scipy
import numpy as np
from scipy import optimize as opt
import matplotlib.pyplot as plt
import math
import random
import sys

sys.path.append('./..')
sys.path.append('./../..')
try:
	import src.tile_definition as tile_definition
	from src.tile_definition import Tile
except:
	import tile_definition as tile_definition
	# from tile_definition import Tile

# ---------------------------------------------------------- #
# Gradient descent with penalty
# ---------------------------------------------------------- #
# Penalty : + Sum (log(beta_ij)
# ---------------------------------------------------------- #


penalty_constant = 2.5

def f(T_set, alpha, beta, membership):
	return


def grad_aux1(T,alpha,beta):
	val = 0
	for ed, r_c  in T.get_elements().items():
		for i in r_c[0]:
			for j in r_c[1]:
				val += alpha[ed][i][j] / (2 * beta[ed][i][j])
	return val

def grad_aux2(T,alpha,beta):
	val = 0
	for ed, r_c  in T.get_elements().items():
		for i in r_c[0]:
			for j in r_c[1]:
				val += (1/2 * beta[ed][i][j]) + (math.pow(alpha[ed][i][j],2) /(4*math.pow(beta[ed][i][j],2)))
	return val

def grad_aux3(T , beta):
	global penalty_constant
	val = 0
	for ed, r_c  in T.get_elements().items():
		for i in r_c[0]:
			for j in r_c[1]:
				val += (1/ beta[ed][i][j])
	return penalty_constant * val


def deriv_f(T_set, alpha, beta, membership):
	grad = np.zeros([len(T_set),2])
	# Note : Reverse sign from paper -> as we are doing a minimization!

	for id, T in T_set.items():
		# lambda_m
		grad[id][0] = T.f_m + grad_aux1(T,alpha,beta)
		grad[id][1] = T.f_v - grad_aux1(T, alpha, beta) - grad_aux3(T , beta)

	return grad


def update_alpha(params, membership):
	_data = Tile.data
	alpha = [np.zeros(_matrix.shape) for _matrix in _data]

	num_ed = len(alpha)
	for i in range(num_ed):
		for j in range(alpha[i].shape[0]):
			for k in range(alpha[i].shape[1]):
				vals = [ params[id][0] for id in membership[i][j][k]]
				alpha[i][j][k] = np.sum(vals)
	return alpha


# T_set is a dictionary { t_id : t_object }
def update_beta(params, membership):
	_data = Tile.data
	beta = [np.zeros(_matrix.shape) for _matrix in _data]

	num_ed = len(beta)
	for i in range(num_ed):
		for j in range(beta[i].shape[0]):
			for k in range(beta[i].shape[1]):
				vals = [params[id][1] for id in membership[i][j][k]]
				beta[i][j][k] = np.sum(vals)
	return beta

# --------------------------------------- #
# This function gets the (i,j)  and the corresponding tile_ids
def get_membership(T_set):
	print('In get_membership ')
	# Create a matrix with same dimensions as the Data
	#  each entry is a list of tids
	_data = Tile.data
	num_entities = len(_data)
	print(num_entities)
	mem = [None] * num_entities
	for e in range(num_entities):
		j = _data[e].shape[0]
		k = _data[e].shape[1]
		arr = [[None] * k] * j  # j rows , k columns

		print('----')
		for _j in range(j):
			for _k in range(k):
				tmp = []
				for t_id, T in T_set.items():
					print(T.get_elements())
					# Tile object check : entity domain
					print(e, _j, _k)
					if T.check(e, _j, _k):
						tmp.append(t_id)

				arr[_j][_k] = tmp

		mem[e] = arr
	return mem
# --------------------------------------- #


def check_positive_beta(beta):
	mins = [np.min(_matrix) for _matrix in beta]

	if np.min(mins) > 0:
		return True
	else:
		return False


# -----------------------------------------------------#
def run_opt(T_set, lr, max_Err, max_iter):
	for id, t_obj in T_set.items():
		print(id, t_obj.get_elements())

	membership = get_membership(T_set)
	# there are 2 params per tile

	params = np.random.random([len(T_set), 2]) + 0.5
	print('Initial Parameters ',params)

	# Initial  values
	for id, t_obj in T_set.items():
		t_obj.lambda_m = params[id][0]
		t_obj.lambda_v = params[id][1]


	# Define alpha_ij s
	alpha = update_alpha(params, membership)
	# Define beta_ij s
	beta = update_beta(params, membership)

	print('Initial alpha', alpha)
	print('Initial beta', beta)
	prev_step = 1
	cur_iter = 0

	while (prev_step > max_Err) and (cur_iter < max_iter):
		print('iteration', cur_iter+1 )
		grad = deriv_f(T_set, alpha, beta, membership)
		new_params = params - grad * lr
		new_beta = update_beta(params, membership)

		if check_positive_beta(new_beta):
			beta = new_beta
			alpha = update_alpha(params, membership)
		else:
			# Random restarts
			print('condition check fails!!')

			exit(1)

		prev_step = np.max(np.abs(new_params - params))
		print('prev_step',prev_step)
		params = new_params
		cur_iter += 1

	return params


# ------------------------------------------------------ #
# Main function to call
# ------------------------------------------------------ #
# Input Tile set
# Dictionary of tiles :
# { tile_id : tile_obj }
# ------------------------------------------------------ #
def optimize(Tile_set):
	lr = 0.002
	max_iter = 10000
	# check convergence
	max_Err = math.pow(10, -3)
	return run_opt(Tile_set, lr, max_Err, max_iter)

