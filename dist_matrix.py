# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu
@license: Apache Licence 
@file: dist_matrix.py 
@time: 2020/10/17
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020
"""

import pandas as pd

dist_df = pd.read_csv(
    '/Users/hurunqiu/project/bs_rebalancing_platform/bs_server/resources/dataset_docked/dist_matrix.csv', index_col=0)
dist_df.columns = dist_df.columns.astype(int)


def get_distance(station_1, station_2):
    return dist_df.at[station_1, station_2]
