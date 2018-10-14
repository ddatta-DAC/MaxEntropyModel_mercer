import sys
import os
import numpy as np

sys.path.append('./..')
sys.path.append('./../..')
try:
	import tile_definition as tile_definition
	from tile_definition import Tile
except:
	import src.tile_definition as tile_definition
	from src.tile_definition import Tile


# Background Information
# T_col
# T_rows
# T_domain
def get_background_tiles(Data):
	# Set the static class variable
	Tile.data = Data
	domains = list(range(len(Data)))

	T_col = []
	for d in domains:
		_data_matrix = Data[d]
		all_rows = list(range(_data_matrix.shape[0]))
		for c in range(_data_matrix.shape[1]):
			t_obj = Tile(domain_idx1=0, domain_idx2=[d])
			t_obj.set_elements(ed=d, r_t=all_rows, c_t=[c])
			T_col.append(t_obj)

	T_row = []
	for d in domains:
		_data_matrix = Data[d]
		all_cols = list(range(_data_matrix.shape[1]))
		for r in range(_data_matrix.shape[0]):
			t_obj = Tile(domain_idx1=0, domain_idx2=[d])
			t_obj.set_elements(ed=d, r_t=[r], c_t=all_cols)
			T_row.append(t_obj)

	T_dom = []
	for d in domains:
		all_rows = list(range(Data[d].shape[0]))
		all_cols = list(range(Data[d].shape[1]))
		t_obj = Tile(domain_idx1=0, domain_idx2=[d])
		t_obj.set_elements(ed=d, r_t=all_rows, c_t=all_cols)
		T_dom.append(t_obj)

	T_back = []
	T_back.extend(T_row)
	T_back.extend(T_col)
	T_back.extend(T_dom)
	return T_back


def get_background_info(D):
	T_back = get_background_tiles(D)
	from collections import OrderedDict
	T_back_dict = OrderedDict()

	for t_obj in T_back:
		T_back_dict[t_obj.tile_id] = t_obj

	T_back_dict = OrderedDict(sorted(T_back_dict.items(), key=lambda t: t[0]))

	return T_back_dict
