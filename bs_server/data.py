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
import numpy as np
import pandas as pd

# from dist_matrix import distance_matrix

pref = None
system = 'mac'
if system == 'mac':
    pref = '~/project/bs_rebalancing_platform/'
else:
    pref = '~/'

distance_matrix = pd.read_csv(pref + "bs_server/resources/dataset_docked/dist_matrix.csv",
                              header=None).to_numpy()

past_rent = np.array(
    [1, 2, 4, 9, 3, 0, 4, 0, 8, 5, 3, 2, 10, 0, 1, 6, 1,
     4, 0, 0, 0, 5, 2, 1, 8, 4, 0, 0, 0, 2, 0, 0, 2, 5,
     3, 2, 6, 1, 2, 0, 4, 0, 1, 1, 2, 8, 1, 6, 4, 0, 0,
     3, 1, 2, 8, 0, 1, 4, 1, 1, 3, 7, 2, 4, 2, 1, 1, 0,
     2, 0, 4, 1, 7, 4, 0, 1, 1, 3, 0, 0, 4, 2, 2, 6, 3,
     17, 1, 1, 9, 5, 12, 0, 1, 1, 7, 2, 5, 0, 5, 0, 7, 4,
     2, 3, 4, 3, 0, 1, 4, 5, 0, 3, 2, 1, 1, 19, 7, 11, 0,
     3, 6, 3, 1, 8, 3, 0, 3, 8, 1, 6, 8, 1, 4, 8, 6, 0,
     0, 3, 3, 3, 3, 3, 11, 2, 2, 1, 1, 3, 3, 1, 0, 5, 8,
     1, 2, 8, 5, 6, 1, 0, 0, 0, 4, 1])
past_return = np.array(
    [0, 22, 0, 2, 8, 1, 13, 1, 2, 1, 3, 1, 4, 2, 2, 2, 2,
     2, 3, 1, 0, 1, 1, 1, 2, 3, 2, 1, 2, 0, 3, 0, 0, 1,
     10, 3, 5, 1, 5, 3, 3, 0, 0, 1, 2, 2, 11, 4, 2, 0, 3,
     2, 6, 4, 5, 2, 1, 1, 1, 2, 1, 6, 0, 2, 4, 0, 1, 0,
     2, 0, 6, 2, 6, 0, 0, 1, 0, 5, 5, 4, 2, 2, 6, 4, 0,
     6, 2, 1, 0, 1, 3, 4, 2, 1, 3, 2, 1, 1, 3, 0, 5, 7,
     4, 0, 5, 2, 0, 1, 6, 1, 0, 4, 2, 5, 6, 4, 5, 3, 5,
     7, 6, 1, 3, 13, 1, 0, 3, 2, 2, 5, 2, 3, 2, 15, 7, 0,
     1, 6, 1, 4, 1, 1, 5, 1, 1, 0, 0, 13, 1, 2, 1, 2, 2,
     3, 2, 1, 4, 2, 0, 0, 1, 0, 1, 2])
pred_rent = np.array(
    [3, 15, 14, 10, 10, 6, 30, 10, 17, 13, 14, 11, 29, 3, 15, 20, 3,
     10, 3, 5, 2, 4, 8, 7, 11, 15, 2, 8, 1, 17, 20, 6, 0, 11,
     12, 10, 22, 15, 19, 11, 6, 0, 8, 1, 11, 16, 10, 9, 21, 6, 12,
     35, 5, 11, 30, 2, 1, 2, 3, 13, 9, 15, 8, 8, 14, 1, 3, 4,
     6, 7, 13, 4, 20, 17, 5, 4, 13, 22, 5, 13, 31, 7, 11, 10, 6,
     58, 4, 11, 34, 12, 48, 21, 2, 7, 29, 10, 9, 7, 35, 1, 17, 16,
     10, 17, 16, 15, 10, 4, 17, 7, 3, 19, 7, 7, 37, 54, 9, 21, 8,
     30, 58, 16, 9, 28, 14, 5, 11, 26, 5, 28, 13, 17, 17, 59, 23, 6,
     12, 13, 10, 3, 3, 13, 39, 5, 5, 4, 4, 13, 3, 7, 13, 6, 26,
     2, 9, 18, 15, 11, 1, 0, 4, 7, 9, 11])
pred_return = np.array(
    [1, 28, 23, 14, 41, 14, 14, 0, 6, 9, 29, 11, 4, 4, 7, 11, 6,
     10, 16, 1, 4, 6, 9, 8, 14, 6, 0, 8, 1, 13, 24, 12, 0, 20,
     12, 16, 22, 9, 9, 14, 13, 0, 11, 4, 3, 38, 38, 26, 16, 5, 12,
     3, 12, 11, 18, 13, 4, 2, 1, 6, 22, 64, 16, 7, 6, 0, 1, 2,
     7, 6, 45, 14, 9, 6, 1, 3, 15, 22, 19, 14, 20, 9, 6, 8, 2,
     25, 2, 18, 4, 3, 29, 20, 18, 6, 19, 10, 14, 11, 14, 29, 15, 16,
     17, 35, 28, 11, 8, 4, 54, 9, 4, 14, 11, 8, 12, 19, 13, 14, 12,
     22, 31, 19, 8, 58, 9, 8, 29, 44, 14, 6, 8, 11, 11, 57, 11, 12,
     13, 19, 3, 4, 2, 14, 14, 17, 15, 2, 2, 18, 9, 12, 7, 3, 11,
     0, 2, 15, 37, 15, 7, 0, 2, 2, 2, 7])


truck_velocity = 420

reserved_time = 5

truck_capacity = 60

station_info = [{'cluster': 1, 'demand': 22, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5, 'priority': 26.83, 'ratio': 0, 'station_id': 98, 'velocity': 0.24, 'warning_time': 0, 'distance': 3.53}, {'cluster': 1, 'demand': 17, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5, 'priority': 26.49, 'ratio': 0, 'station_id': 162, 'velocity': 0.16, 'warning_time': 0, 'distance': 2.61}, {'cluster': 1, 'demand': 40, 'diversity': None, 'full_empty_time': 9.35, 'key_distance': None, 'latest_time': 14.35, 'priority': 26.14, 'ratio': 0.17, 'station_id': 85, 'velocity': 0.64, 'warning_time': 0, 'distance': 4.58}, {'cluster': 1, 'demand': 49, 'diversity': None, 'full_empty_time': 10.11, 'key_distance': None, 'latest_time': 15.11, 'priority': 25.81, 'ratio': 0.18, 'station_id': 115, 'velocity': 0.79, 'warning_time': 0, 'distance': 2.62}, {'cluster': 1, 'demand': -15, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5, 'priority': 25.47, 'ratio': 1, 'station_id': 92, 'velocity': -0.17, 'warning_time': 0, 'distance': 0.55}, {'cluster': 1, 'demand': 13, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5, 'priority': 25.15, 'ratio': 0, 'station_id': 42, 'velocity': 0.01, 'warning_time': 0, 'distance': 3.32}, {'cluster': 1, 'demand': -11, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5, 'priority': 24.82, 'ratio': 1.17, 'station_id': 145, 'velocity': 0.05, 'warning_time': 0, 'distance': 2.78}, {'cluster': 1, 'demand': -10, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5, 'priority': 24.5, 'ratio': 1, 'station_id': 131, 'velocity': -0.02, 'warning_time': 0, 'distance': 0.55}, {'cluster': 1, 'demand': 4, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5, 'priority': 24.18, 'ratio': 0, 'station_id': 13, 'velocity': -0.08, 'warning_time': 0, 'distance': 1.73}, {'cluster': 1, 'demand': 29, 'diversity': None, 'full_empty_time': 18.18, 'key_distance': None, 'latest_time': 23.18, 'priority': 23.87, 'ratio': 0.33, 'station_id': 88, 'velocity': 0.55, 'warning_time': 7.27, 'distance': 0.55}, {'cluster': 1, 'demand': -39, 'diversity': None, 'full_empty_time': 21.94, 'key_distance': None, 'latest_time': 26.94, 'priority': 23.56, 'ratio': 0.62, 'station_id': 1, 'velocity': -0.77, 'warning_time': 10.32, 'distance': 2.28}, {'cluster': 1, 'demand': 21, 'diversity': None, 'full_empty_time': 29.39, 'key_distance': None, 'latest_time': 34.39, 'priority': 23.26, 'ratio': 0.3, 'station_id': 142, 'velocity': 0.41, 'warning_time': 9.8, 'distance': 2.2}, {'cluster': 1, 'demand': 18, 'diversity': None, 'full_empty_time': 30, 'key_distance': None, 'latest_time': 35, 'priority': 22.96, 'ratio': 0.2, 'station_id': 51, 'velocity': 0.3, 'warning_time': 0.67, 'distance': 1.32}, {'cluster': 1, 'demand': -24, 'diversity': None, 'full_empty_time': 33.53, 'key_distance': None, 'latest_time': 38.53, 'priority': 22.66, 'ratio': 0.55, 'station_id': 46, 'velocity': -0.57, 'warning_time': 18.71, 'distance': 2.8}, {'cluster': 1, 'demand': 14, 'diversity': None, 'full_empty_time': 34.29, 'key_distance': None, 'latest_time': 39.29, 'priority': 22.37, 'ratio': 0.13, 'station_id': 24, 'velocity': 0.18, 'warning_time': 0, 'distance': 3.21}, {'cluster': 1, 'demand': 11, 'diversity': None, 'full_empty_time': 40, 'key_distance': None, 'latest_time': 45, 'priority': 22.08, 'ratio': 0.04, 'station_id': 0, 'velocity': 0.05, 'warning_time': 0, 'distance': 2.03}, {'cluster': 1, 'demand': 10, 'diversity': None, 'full_empty_time': 40, 'key_distance': None, 'latest_time': 45, 'priority': 21.8, 'ratio': 0.11, 'station_id': 57, 'velocity': 0.1, 'warning_time': 0, 'distance': 2.65}, {'cluster': 1, 'demand': 13, 'diversity': None, 'full_empty_time': 42.86, 'key_distance': None, 'latest_time': 47.86, 'priority': 21.52, 'ratio': 0.09, 'station_id': 109, 'velocity': 0.12, 'warning_time': 0, 'distance': 2.03}, {'cluster': 1, 'demand': -16, 'diversity': None, 'full_empty_time': 43.2, 'key_distance': None, 'latest_time': 48.2, 'priority': 21.24, 'ratio': 0.59, 'station_id': 123, 'velocity': -0.42, 'warning_time': 22.08, 'distance': 1.67}, {'cluster': 1, 'demand': 9, 'diversity': None, 'full_empty_time': 43.2, 'key_distance': None, 'latest_time': 48.2, 'priority': 20.96, 'ratio': 0.33, 'station_id': 15, 'velocity': 0.21, 'warning_time': 17.28, 'distance': 1.78}, {'cluster': 1, 'demand': 11, 'diversity': None, 'full_empty_time': 45.52, 'key_distance': None, 'latest_time': 50.52, 'priority': 20.69, 'ratio': 0.31, 'station_id': 130, 'velocity': 0.24, 'warning_time': 16.55, 'distance': 3.18}, {'cluster': 1, 'demand': 12, 'diversity': None, 'full_empty_time': 46.15, 'key_distance': None, 'latest_time': 51.15, 'priority': 20.43, 'ratio': 0.43, 'station_id': 152, 'velocity': 0.32, 'warning_time': 24.62, 'distance': 1.21}, {'cluster': 1, 'demand': 10, 'diversity': None, 'full_empty_time': 50, 'key_distance': None, 'latest_time': 55, 'priority': 20.16, 'ratio': 0.12, 'station_id': 29, 'velocity': 0.1, 'warning_time': 0, 'distance': 2.4}, {'cluster': 1, 'demand': 12, 'diversity': None, 'full_empty_time': 53.33, 'key_distance': None, 'latest_time': 58.33, 'priority': 19.9, 'ratio': 0.25, 'station_id': 73, 'velocity': 0.22, 'warning_time': 10.67, 'distance': 3.18}, {'cluster': 1, 'demand': 8, 'diversity': None, 'full_empty_time': 55.38, 'key_distance': None, 'latest_time': 60.38, 'priority': 19.65, 'ratio': 0.38, 'station_id': 94, 'velocity': 0.22, 'warning_time': 25.85, 'distance': 1.45}, {'cluster': 1, 'demand': -7, 'diversity': None, 'full_empty_time': 56.47, 'key_distance': None, 'latest_time': 61.47, 'priority': 19.39, 'ratio': 0.71, 'station_id': 113, 'velocity': -0.14, 'warning_time': 16.94, 'distance': 2.13}, {'cluster': 1, 'demand': 12, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65, 'priority': 19.14, 'ratio': 0.12, 'station_id': 21, 'velocity': 0.12, 'warning_time': 0, 'distance': 1.24}, {'cluster': 1, 'demand': -8, 'diversity': None, 'full_empty_time': 57, 'key_distance': None, 'latest_time': 62, 'priority': 18.9, 'ratio': 0.46, 'station_id': 70, 'velocity': -0.33, 'warning_time': 36, 'distance': 3.38}, {'cluster': 1, 'demand': 12, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65, 'priority': 18.65, 'ratio': 0.04, 'station_id': 14, 'velocity': 0.03, 'warning_time': 0, 'distance': 2.33}, {'cluster': 1, 'demand': 10, 'diversity': None, 'full_empty_time': 58.29, 'key_distance': None, 'latest_time': 63.29, 'priority': 18.41, 'ratio': 0.38, 'station_id': 8, 'velocity': 0.29, 'warning_time': 27.43, 'distance': 3.17}, {'cluster': 1, 'demand': -8, 'diversity': None, 'full_empty_time': 57.78, 'key_distance': None, 'latest_time': 62.78, 'priority': 18.17, 'ratio': 0.63, 'station_id': 52, 'velocity': -0.22, 'warning_time': 26.67, 'distance': 2.72}, {'cluster': 1, 'demand': 10, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65, 'priority': 17.94, 'ratio': 0.21, 'station_id': 9, 'velocity': 0.17, 'warning_time': 2.4, 'distance': 2.82}, {'cluster': 1, 'demand': 10, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65, 'priority': 17.71, 'ratio': 0.17, 'station_id': 138, 'velocity': 0.12, 'warning_time': 0, 'distance': 2.93}, {'cluster': 1, 'demand': -6, 'diversity': None, 'full_empty_time': 57.6, 'key_distance': None, 'latest_time': 62.6, 'priority': 17.48, 'ratio': 0.56, 'station_id': 18, 'velocity': -0.21, 'warning_time': 31.68, 'distance': 3.75}, {'cluster': 1, 'demand': 9, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65, 'priority': 17.25, 'ratio': 0.04, 'station_id': 58, 'velocity': 0.02, 'warning_time': 0, 'distance': 3.32}, {'cluster': 1, 'demand': 7, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65, 'priority': 17.03, 'ratio': 0.15, 'station_id': 37, 'velocity': 0.05, 'warning_time': 0, 'distance': 0.84}, {'cluster': 1, 'demand': 8, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65, 'priority': 16.81, 'ratio': 0.21, 'station_id': 84, 'velocity': 0.13, 'warning_time': 3, 'distance': 2.24}, {'cluster': 1, 'demand': 8, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65, 'priority': 16.59, 'ratio': 0.12, 'station_id': 17, 'velocity': 0.07, 'warning_time': 0, 'distance': 2.98}]


distance_matrix = distance_matrix

initial_bike = np.array(
    [[2, 17, 6, 14, 12, 5, 20, 19, 11, 5, 5, 3, 28, 0, 2, 5,
      17, 1, 11, 3, 3, 5, 1, 1, 2, 4, 5, 6, 1, 7, 12, 6,
      8, 5, 10, 16, 3, 2, 9, 9, 12, 5, 0, 3, 3, 9, 7, 12,
      11, 21, 11, 12, 12, 8, 9, 12, 4, 2, 1, 2, 10, 5, 4, 5,
      4, 15, 8, 10, 8, 8, 6, 7, 9, 8, 10, 4, 5, 11, 9, 10,
      14, 14, 8, 7, 6, 3, 21, 7, 7, 23, 28, 20, 15, 2, 7, 10,
      7, 12, 0, 16, 17, 2, 6, 12, 10, 9, 16, 7, 3, 2, 9, 6,
      5, 11, 7, 9, 30, 24, 7, 7, 8, 16, 26, 13, 5, 17, 12, 7,
      10, 11, 2, 32, 12, 23, 10, 25, 12, 0, 3, 7, 5, 17, 2, 2,
      12, 41, 7, 0, 10, 3, 6, 4, 12, 2, 0, 28, 5, 8, 7, 9,
      2, 1, 0, 6, 9, 5, 12],
     [2, 17, 6, 15, 14, 6, 22, 25, 13, 5, 6, 6, 28, 0, 2, 5,
      19, 1, 12, 5, 6, 6, 2, 2, 3, 5, 5, 9, 1, 8, 14, 7,
      8, 7, 11, 19, 3, 2, 10, 14, 16, 6, 0, 3, 7, 10, 7, 15,
      13, 23, 13, 13, 16, 11, 11, 15, 4, 2, 1, 7, 12, 6, 6, 6,
      6, 20, 13, 14, 10, 8, 6, 7, 9, 8, 11, 4, 8, 13, 8, 14,
      16, 15, 9, 8, 8, 3, 23, 8, 7, 23, 36, 22, 16, 2, 9, 17,
      8, 15, 0, 20, 18, 2, 7, 14, 11, 9, 17, 9, 3, 4, 17, 7,
      6, 18, 8, 9, 38, 24, 8, 10, 11, 21, 28, 16, 7, 17, 17, 8,
      12, 11, 3, 42, 12, 31, 15, 27, 12, 0, 3, 8, 6, 18, 2, 2,
      12, 46, 9, 1, 12, 5, 17, 7, 13, 2, 4, 33, 5, 10, 12, 9,
      2, 2, 0, 9, 9, 5, 15],
     [2, 28, 25, 14, 15, 13, 32, 19, 17, 12, 17, 10, 36, 0, 2, 9,
      19, 5, 15, 7, 5, 7, 8, 6, 6, 11, 10, 9, 2, 5, 15, 17,
      9, 7, 15, 23, 8, 9, 16, 11, 19, 22, 0, 8, 11, 14, 23, 18,
      19, 34, 12, 9, 22, 14, 14, 23, 10, 4, 2, 6, 16, 6, 19, 13,
      14, 18, 9, 14, 12, 11, 16, 18, 19, 12, 14, 4, 7, 19, 24, 22,
      19, 15, 13, 10, 12, 6, 24, 13, 10, 28, 46, 25, 21, 11, 12, 26,
      15, 19, 0, 21, 24, 5, 17, 18, 17, 19, 31, 18, 6, 5, 28, 11,
      9, 20, 7, 8, 49, 27, 13, 19, 19, 18, 30, 26, 10, 32, 15, 14,
      28, 19, 11, 42, 14, 30, 16, 36, 15, 0, 8, 12, 18, 20, 12, 3,
      19, 42, 10, 2, 16, 4, 23, 15, 15, 6, 5, 36, 9, 11, 15, 19,
      14, 3, 0, 8, 11, 5, 20],
     []])[2]

max_capacity = np.array([48, 45, 60, 31, 47, 42, 55, 29, 45, 58, 42, 41, 30, 40, 57, 27,
                         47, 42, 27, 48, 44, 60, 45, 49, 47, 26, 40, 29, 59, 42, 52, 41,
                         36, 35, 31, 41, 42, 62, 27, 34, 59, 45, 60, 58, 46, 41, 42, 37,
                         48, 58, 40, 44, 35, 29, 31, 62, 29, 38, 50, 25, 48, 53, 36, 34,
                         52, 22, 42, 48, 41, 49, 35, 41, 41, 48, 35, 43, 41, 35, 64, 45,
                         41, 61, 34, 36, 58, 35, 41, 45, 30, 28, 52, 46, 21, 32, 32, 30,
                         23, 26, 33, 42, 46, 34, 36, 39, 39, 41, 36, 60, 39, 53, 45, 19,
                         30, 28, 32, 45, 50, 28, 47, 41, 37, 24, 56, 44, 44, 34, 40, 41,
                         39, 41, 35, 42, 39, 45, 20, 58, 43, 30, 48, 26, 25, 27, 40, 49,
                         51, 36, 56, 34, 34, 37, 48, 34, 35, 35, 39, 58, 58, 58, 51, 24,
                         37, 33, 37, 31])

travel_cost = 0.42
working_cost = 0.67

lat_lon = pd.read_csv(
    pref + 'bs_server/resources/dataset_dockless/lat_lon.csv',
    header=0, usecols=[1, 2]).to_numpy()

final_station_info = {}
for item in station_info:
    final_station_info[item['station_id']] = item
    final_station_info[item['station_id']]['max_capacity'] = max_capacity[item['station_id']]
    final_station_info[item['station_id']]['init_inventory'] = initial_bike[item['station_id']]
    final_station_info[item['station_id']].pop('station_id')

station_info = final_station_info
station_list = list(station_info.keys())
print(station_list)
# station_list = list(station_info.keys())
# for i in range(38):
#     print(station_list[i])

# print(list(station_info.keys()))

# center = [(118.7931074, 32.04722081), (118.7860483, 32.02286646), (118.7721501, 32.06339912),
#           (118.7752358, 32.04127961)]

center = (32.057458085043166, 118.77314443822803)
