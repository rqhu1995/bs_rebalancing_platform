# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu
@license: Apache Licence 
@file: data_dockless.py 
@time: 2020/11/01
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020
"""
# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu
@license: Apache Licence 
@file: data.py
@time: 2020/10/07
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020
"""
import pandas as pd

# from dist_matrix import distance_matrix

pref = None
system = 'mac'
if system == 'mac':
    pref = '~/project/bs_rebalancing_platform/'
else:
    pref = '~/'

distance_matrix = pd.read_csv(pref + "bs_server/resources/dataset_dockless/station_dist_matrix_300.csv",
                              header=None).to_numpy()

truck_velocity = 420

reserved_time = 5

truck_capacity = 60

stage = 0

travel_cost = 0.42
working_cost = 0.67

lat_lon = pd.read_csv(
    pref + 'bs_server/resources/dataset_dockless/lat_lon.csv',
    header=0, usecols=[1, 2]).to_numpy()


center = (32.057458085043166, 118.77314443822803)

