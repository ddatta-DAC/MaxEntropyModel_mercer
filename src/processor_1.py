import sys
sys.path.append('./..')
sys.path.append('./../..')
import wwf_2.src.data_fetcher as data_fetcher
import biclustering_1.src.Rinclose_chv as biclustering
import numpy as np
import pandas as pd



# -------------------- #

data_arr, entity_attrs, entity_files = data_fetcher.fetch_data()
print (' Size of the data ', [d.shape for d in data_arr])

res = biclustering.get_chv_bc(data_arr[0], min_rows = 3, epsilon =0.001)
print(res)
