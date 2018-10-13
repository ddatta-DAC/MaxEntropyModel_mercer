import scipy
import numpy as np
from scipy import optimize as opt
import matplotlib.pyplot as plt

'''
https://people.duke.edu/~ccc14/sta-663/BlackBoxOptimization.html
'''


def f(x,a):
	return -(2 * x[0] * x[1] + 2 * x[0] - x[0] ** 2 - 2 * x[1] ** 2)

def deriv(x,a):

	return

constraints = ({
	'type': 'ineq',
	'fun':
}
)

x0 = [0, 2.5]
a = 10
ux = opt.minimize(
	func=f,
	args=(a),
	x0=x0,
	jac=deriv,
	constraints=constraints
)
print(ux)
