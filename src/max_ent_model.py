import scipy
import numpy as np
import sys
sys.path.append('./..')
sys.path.append('./../..')

import src.optimization1
import src.tile_definition as tile_def
from src.tile_definition import Tile
import src.background_tile_info as background
import src.optimization2 as opt

# --------------- #

def get_data( ):
	D = [
		np.random.random([4, 4]),
		np.random.random([4, 6]),
		np.random.random([4, 7]),
		np.random.random([4, 4])
	]
	return D

Data = get_data( )
Tile.data  = Data
print (Data)
T_set = background.get_background_info(Data)
print(' number of tiles ', len(T_set))
params = opt.optimize(T_set)
print(params)
