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

distance_matrix = pd.read_csv("/Users/hurunqiu/aaai/ffbs_dynamic/resources/data_set/station_dist_matrix_300.csv",
                              header=None).to_numpy()

truck_velocity = 420

reserved_time = 5

truck_capacity = 60

station_info = [
    {'cluster': 3, 'demand': 12, 'diversity': None, 'full_empty_time': 40, 'key_distance': None, 'latest_time': 45,
     'priority': 1.41, 'ratio': 0.18, 'station_id': 2, 'velocity': 0.18, 'warning_time': 0, 'distance': 0.52},
    {'cluster': 3, 'demand': 82, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.63, 'ratio': 0, 'station_id': 5, 'velocity': 1.02, 'warning_time': 0, 'distance': 1.39},
    {'cluster': 3, 'demand': 3, 'diversity': None, 'full_empty_time': 53.33, 'key_distance': None, 'latest_time': 58.33,
     'priority': 1.06, 'ratio': 0.36, 'station_id': 13, 'velocity': 0.08, 'warning_time': 24, 'distance': 1.03},
    {'cluster': 3, 'demand': 9, 'diversity': None, 'full_empty_time': 38.18, 'key_distance': None, 'latest_time': 43.18,
     'priority': 1.39, 'ratio': 0.3, 'station_id': 14, 'velocity': 0.18, 'warning_time': 13.09, 'distance': 0.46},
    {'cluster': 3, 'demand': 13, 'diversity': None, 'full_empty_time': 28.8, 'key_distance': None, 'latest_time': 33.8,
     'priority': 1.48, 'ratio': 0.19, 'station_id': 17, 'velocity': 0.21, 'warning_time': 0, 'distance': 0.94},
    {'cluster': 3, 'demand': 12, 'diversity': None, 'full_empty_time': 30, 'key_distance': None, 'latest_time': 35,
     'priority': 1.43, 'ratio': 0.42, 'station_id': 22, 'velocity': 0.27, 'warning_time': 15.75, 'distance': 1.32},
    {'cluster': 3, 'demand': -19, 'diversity': None, 'full_empty_time': 18, 'key_distance': None, 'latest_time': 23,
     'priority': 1.7, 'ratio': 0.71, 'station_id': 26, 'velocity': -0.33, 'warning_time': 5.4, 'distance': 0.71},
    {'cluster': 3, 'demand': 3, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.03, 'ratio': 0.71, 'station_id': 32, 'velocity': 0.22, 'warning_time': 48, 'distance': 1.0},
    {'cluster': 3, 'demand': 6, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.0, 'ratio': 0.19, 'station_id': 38, 'velocity': -0.18, 'warning_time': 0, 'distance': 1.72},
    {'cluster': 3, 'demand': -23, 'diversity': None, 'full_empty_time': 3.33, 'key_distance': None, 'latest_time': 8.33,
     'priority': 1.99, 'ratio': 0.96, 'station_id': 40, 'velocity': -0.3, 'warning_time': 0, 'distance': 1.41},
    {'cluster': 3, 'demand': 14, 'diversity': None, 'full_empty_time': 30, 'key_distance': None, 'latest_time': 35,
     'priority': 1.55, 'ratio': 0.3, 'station_id': 48, 'velocity': 0.27, 'warning_time': 9.75, 'distance': 0.71},
    {'cluster': 3, 'demand': 12, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 1.67, 'ratio': 0, 'station_id': 55, 'velocity': 0.15, 'warning_time': 0, 'distance': 1.45},
    {'cluster': 3, 'demand': 5, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.05, 'ratio': 0.08, 'station_id': 56, 'velocity': 0.02, 'warning_time': 0, 'distance': 1.08},
    {'cluster': 3, 'demand': -8, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 1.65, 'ratio': 1.22, 'station_id': 59, 'velocity': 0, 'warning_time': 0, 'distance': 0.7},
    {'cluster': 3, 'demand': -10, 'diversity': None, 'full_empty_time': 20, 'key_distance': None, 'latest_time': 25,
     'priority': 1.52, 'ratio': 0.82, 'station_id': 63, 'velocity': -0.15, 'warning_time': 0, 'distance': 1.11},
    {'cluster': 3, 'demand': 90, 'diversity': None, 'full_empty_time': 9, 'key_distance': None, 'latest_time': 14,
     'priority': 2.68, 'ratio': 0.11, 'station_id': 69, 'velocity': 1.33, 'warning_time': 0, 'distance': 0.48},
    {'cluster': 3, 'demand': -7, 'diversity': None, 'full_empty_time': 45, 'key_distance': None, 'latest_time': 50,
     'priority': 1.12, 'ratio': 0.75, 'station_id': 70, 'velocity': -0.13, 'warning_time': 9, 'distance': 1.61},
    {'cluster': 3, 'demand': -11, 'diversity': None, 'full_empty_time': 20, 'key_distance': None, 'latest_time': 25,
     'priority': 1.5, 'ratio': 0.86, 'station_id': 75, 'velocity': -0.15, 'warning_time': 0, 'distance': 1.51},
    {'cluster': 3, 'demand': -23, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.12, 'ratio': 1.15, 'station_id': 83, 'velocity': -0.22, 'warning_time': 0, 'distance': 0.21},
    {'cluster': 3, 'demand': 13, 'diversity': None, 'full_empty_time': 56.67, 'key_distance': None,
     'latest_time': 61.67, 'priority': 1.32, 'ratio': 0.29, 'station_id': 87, 'velocity': 0.3, 'warning_time': 17.33,
     'distance': 0.76},
    {'cluster': 3, 'demand': 1, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.1, 'ratio': 0.26, 'station_id': 89, 'velocity': 0.02, 'warning_time': 56, 'distance': 0.82},
    {'cluster': 3, 'demand': 21, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 1.96, 'ratio': 0, 'station_id': 95, 'velocity': 0.22, 'warning_time': 0, 'distance': 1.17},
    {'cluster': 3, 'demand': -49, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.48, 'ratio': 1.61, 'station_id': 97, 'velocity': -0.37, 'warning_time': 0, 'distance': 1.27},
    {'cluster': 3, 'demand': -35, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.36, 'ratio': 1.64, 'station_id': 98, 'velocity': -0.23, 'warning_time': 0, 'distance': 1.49},
    {'cluster': 3, 'demand': 5, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 1.62, 'ratio': 0, 'station_id': 115, 'velocity': 0.02, 'warning_time': 0, 'distance': 1.47},
    {'cluster': 3, 'demand': -16, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.35, 'ratio': 0.82, 'station_id': 117, 'velocity': 0.02, 'warning_time': 0, 'distance': 1.3},
    {'cluster': 3, 'demand': -16, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.45, 'ratio': 0.84, 'station_id': 122, 'velocity': 0.01, 'warning_time': 0, 'distance': 0.19},
    {'cluster': 3, 'demand': -13, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 1.76, 'ratio': 1.36, 'station_id': 126, 'velocity': -0.08, 'warning_time': 0, 'distance': 1.59},
    {'cluster': 3, 'demand': 3, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.15, 'ratio': 0.27, 'station_id': 135, 'velocity': 0.05, 'warning_time': 16, 'distance': 0.66},
    {'cluster': 3, 'demand': -44, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.44, 'ratio': 1.55, 'station_id': 137, 'velocity': -0.18, 'warning_time': 0, 'distance': 1.08},
    {'cluster': 3, 'demand': -8, 'diversity': None, 'full_empty_time': 42.35, 'key_distance': None,
     'latest_time': 47.35, 'priority': 1.37, 'ratio': 0.78, 'station_id': 139, 'velocity': -0.14, 'warning_time': 4.24,
     'distance': 0.43},
    {'cluster': 3, 'demand': -16, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 1.87, 'ratio': 1.62, 'station_id': 142, 'velocity': 0.05, 'warning_time': 0, 'distance': 0.77},
    {'cluster': 3, 'demand': -28, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.18, 'ratio': 1.42, 'station_id': 152, 'velocity': -0.26, 'warning_time': 0, 'distance': 1.76},
    {'cluster': 3, 'demand': 2, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.08, 'ratio': 0.89, 'station_id': 153, 'velocity': 0.25, 'warning_time': 0, 'distance': 0.89},
    {'cluster': 3, 'demand': -34, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.4, 'ratio': 1.13, 'station_id': 162, 'velocity': -0.34, 'warning_time': 0, 'distance': 0.77},
    {'cluster': 3, 'demand': 15, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 1.84, 'ratio': 0, 'station_id': 167, 'velocity': 0.18, 'warning_time': 0, 'distance': 0.98},
    {'cluster': 3, 'demand': -8, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.24, 'ratio': 0.37, 'station_id': 170, 'velocity': -0.77, 'warning_time': 49.83, 'distance': 0.49},
    {'cluster': 3, 'demand': -10, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.13, 'ratio': 0.84, 'station_id': 172, 'velocity': -0.11, 'warning_time': 0, 'distance': 1.31},
    {'cluster': 3, 'demand': 4, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.19, 'ratio': 0.53, 'station_id': 177, 'velocity': 0.23, 'warning_time': 42.86, 'distance': 0.6},
    {'cluster': 3, 'demand': -10, 'diversity': None, 'full_empty_time': 58.06, 'key_distance': None,
     'latest_time': 63.06, 'priority': 1.21, 'ratio': 0.67, 'station_id': 180, 'velocity': -0.26, 'warning_time': 23.23,
     'distance': 1.11},
    {'cluster': 3, 'demand': 3, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 1.6, 'ratio': 0, 'station_id': 183, 'velocity': 0.02, 'warning_time': 0, 'distance': 1.19},
    {'cluster': 3, 'demand': 56, 'diversity': None, 'full_empty_time': 3.04, 'key_distance': None, 'latest_time': 8.04,
     'priority': 2.51, 'ratio': 0.02, 'station_id': 188, 'velocity': 0.66, 'warning_time': 0, 'distance': 0.33},
    {'cluster': 3, 'demand': -1, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.02, 'ratio': 0.77, 'station_id': 195, 'velocity': -0.02, 'warning_time': 40, 'distance': 0.96},
    {'cluster': 3, 'demand': -1, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.26, 'ratio': 0.52, 'station_id': 196, 'velocity': -0.14, 'warning_time': 57.88, 'distance': 0.09},
    {'cluster': 3, 'demand': -10, 'diversity': None, 'full_empty_time': 40, 'key_distance': None, 'latest_time': 45,
     'priority': 1.3, 'ratio': 0.85, 'station_id': 203, 'velocity': -0.12, 'warning_time': 0, 'distance': 0.97},
    {'cluster': 3, 'demand': -19, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 1.93, 'ratio': 1.48, 'station_id': 207, 'velocity': -0.08, 'warning_time': 0, 'distance': 1.12},
    {'cluster': 3, 'demand': 60, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.55, 'ratio': 0, 'station_id': 214, 'velocity': 0.77, 'warning_time': 0, 'distance': 1.32},
    {'cluster': 3, 'demand': 76, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.59, 'ratio': 0, 'station_id': 222, 'velocity': 0.96, 'warning_time': 0, 'distance': 0.49},
    {'cluster': 3, 'demand': 12, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 1.73, 'ratio': 0, 'station_id': 228, 'velocity': 0.12, 'warning_time': 0, 'distance': 1.23},
    {'cluster': 3, 'demand': -7, 'diversity': None, 'full_empty_time': 33.33, 'key_distance': None,
     'latest_time': 38.33, 'priority': 1.28, 'ratio': 0.62, 'station_id': 230, 'velocity': -0.15, 'warning_time': 16,
     'distance': 1.46},
    {'cluster': 3, 'demand': 26, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.15, 'ratio': 0, 'station_id': 232, 'velocity': 0.28, 'warning_time': 0, 'distance': 0.96},
    {'cluster': 3, 'demand': 13, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 1.78, 'ratio': 0, 'station_id': 233, 'velocity': 0.13, 'warning_time': 0, 'distance': 1.12},
    {'cluster': 3, 'demand': -28, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.22, 'ratio': 1.89, 'station_id': 237, 'velocity': -0.11, 'warning_time': 0, 'distance': 0.85},
    {'cluster': 3, 'demand': 34, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.33, 'ratio': 0, 'station_id': 241, 'velocity': -0.04, 'warning_time': 0, 'distance': 0.97},
    {'cluster': 3, 'demand': -23, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.08, 'ratio': 1.3, 'station_id': 254, 'velocity': -0.16, 'warning_time': 0, 'distance': 0.35},
    {'cluster': 3, 'demand': 13, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.23, 'ratio': 0.2, 'station_id': 263, 'velocity': -0.03, 'warning_time': 0, 'distance': 1.24},
    {'cluster': 3, 'demand': -24, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.02, 'ratio': 1.67, 'station_id': 267, 'velocity': -0.12, 'warning_time': 0, 'distance': 1.03},
    {'cluster': 3, 'demand': -18, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 1.9, 'ratio': 1.27, 'station_id': 283, 'velocity': -0.12, 'warning_time': 0, 'distance': 1.07},
    {'cluster': 3, 'demand': -38, 'diversity': None, 'full_empty_time': 26.81, 'key_distance': None,
     'latest_time': 31.81, 'priority': 2.29, 'ratio': 0.65, 'station_id': 284, 'velocity': -0.78, 'warning_time': 11.49,
     'distance': 1.34},
    {'cluster': 3, 'demand': 25, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.05, 'ratio': 0, 'station_id': 285, 'velocity': -0.38, 'warning_time': 0, 'distance': 1.16},
    {'cluster': 3, 'demand': 28, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 2.25, 'ratio': 0, 'station_id': 286, 'velocity': 0.33, 'warning_time': 0, 'distance': 0.74},
    {'cluster': 3, 'demand': 3, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 1.57, 'ratio': 0, 'station_id': 292, 'velocity': -0.05, 'warning_time': 0, 'distance': 1.44},
    {'cluster': 3, 'demand': 5, 'diversity': None, 'full_empty_time': 60, 'key_distance': None, 'latest_time': 65,
     'priority': 1.17, 'ratio': 0.29, 'station_id': 296, 'velocity': 0.13, 'warning_time': 24, 'distance': 0.65},
    {'cluster': 3, 'demand': -15, 'diversity': None, 'full_empty_time': 0, 'key_distance': None, 'latest_time': 5,
     'priority': 1.81, 'ratio': 1.12, 'station_id': 298, 'velocity': -0.16, 'warning_time': 0, 'distance': 1.34}]

initial_bike = np.array((
    [2, 25, 7, 17, 10, 0, 0, 35, 15, 60, 22, 6, 39, 4, 7, 0, 48, 6, 15, 0, 37, 16, 8, 4, 12, 22, 15, 12, 1, 15, 23, 30,
     15, 75, 77, 29, 63, 0, 5, 0, 25, 25, 17, 0, 42, 4, 29, 15, 8, 9, 14, 30, 26, 23, 31, 0, 2, 40, 2, 22, 13, 28, 0,
     14, 16, 32, 24, 32, 12, 12, 18, 13, 25, 3, 19, 18, 0, 15, 8, 0, 3, 45, 57, 30, 34, 8, 17, 17, 23, 6, 2, 23, 15, 28,
     42, 0, 18, 53, 41, 19, 18, 40, 16, 22, 13, 4, 16, 10, 10, 1, 27, 18, 11, 15, 44, 0, 4, 23, 0, 10, 43, 12, 21, 0, 5,
     0, 19, 11, 46, 11, 30, 0, 11, 26, 0, 3, 21, 68, 2, 21, 5, 10, 21, 27, 0, 21, 16, 10, 42, 0, 2, 18, 27, 17, 58, 0,
     31, 30, 0, 0, 49, 0, 44, 61, 44, 25, 62, 0, 12, 0, 33, 44, 68, 37, 10, 0, 46, 16, 8, 0, 30, 0, 29, 0, 0, 5, 27, 47,
     2, 0, 7, 42, 31, 22, 0, 23, 15, 11, 37, 22, 21, 3, 0, 29, 40, 21, 48, 31, 21, 17, 42, 58, 10, 24, 0, 0, 10, 19, 0,
     0, 45, 0, 0, 43, 3, 0, 42, 28, 0, 10, 8, 3, 0, 0, 59, 15, 16, 36, 8, 0, 52, 0, 24, 12, 41, 18, 13, 27, 33, 65, 0,
     13, 15, 45, 35, 15, 0, 4, 61, 0, 17, 0, 7, 5, 0, 0, 0, 30, 0, 2, 23, 0, 62, 28, 0, 0, 14, 5, 20, 2, 0, 58, 20, 28,
     39, 0, 0, 18, 28, 12, 26, 0, 0, 0, 0, 0, 10, 15, 18, 17]))

max_capacity = np.array([57, 36, 38, 20, 51, 98, 30, 104, 37, 68, 18, 67, 35,
                         11, 23, 20, 61, 32, 27, 54, 64, 22, 19, 45, 42, 76,
                         21, 50, 11, 57, 16, 43, 21, 53, 44, 18, 44, 61, 27,
                         106, 26, 79, 57, 23, 40, 34, 25, 40, 27, 21, 31, 51,
                         59, 40, 50, 14, 26, 52, 9, 18, 36, 46, 68, 17, 27,
                         51, 40, 45, 14, 106, 24, 33, 26, 79, 42, 21, 50, 21,
                         12, 36, 32, 53, 43, 26, 53, 18, 37, 59, 29, 23, 36,
                         50, 14, 39, 35, 37, 73, 33, 25, 43, 128, 34, 40, 30,
                         32, 87, 24, 38, 29, 57, 29, 39, 41, 53, 35, 14, 52,
                         28, 55, 81, 75, 21, 25, 55, 30, 146, 14, 36, 35, 40,
                         28, 40, 43, 35, 33, 11, 31, 44, 44, 27, 23, 27, 13,
                         47, 51, 100, 28, 46, 24, 6, 23, 42, 19, 19, 62, 49,
                         20, 56, 50, 52, 38, 54, 39, 43, 40, 28, 63, 19, 61,
                         39, 89, 37, 81, 40, 13, 51, 46, 30, 44, 91, 45, 62,
                         29, 9, 57, 44, 32, 33, 89, 78, 58, 40, 53, 57, 72,
                         30, 29, 58, 22, 33, 41, 23, 35, 34, 56, 29, 50, 21,
                         38, 46, 35, 59, 39, 38, 70, 60, 38, 49, 40, 30, 43,
                         78, 91, 27, 65, 34, 40, 31, 23, 43, 13, 65, 47, 24,
                         45, 117, 53, 19, 41, 79, 53, 45, 33, 24, 41, 51, 32,
                         22, 37, 54, 119, 30, 44, 31, 27, 32, 49, 53, 34, 34,
                         40, 67, 39, 25, 62, 82, 50, 18, 48, 39, 41, 59, 46,
                         59, 70, 66, 23, 27, 13, 37, 35, 53, 44, 22, 60, 59,
                         38, 47, 32, 65, 62, 60, 7, 85, 54, 48, 34, 26, 16,
                         29])

travel_cost = 0.42
working_cost = 0.67

station_count = 300

lat_lon = pd.read_csv('/Users/hurunqiu/project/bs_rebalancing_platform/bs_server/resources/dataset/lat_lon.csv',
                      header=0, usecols=[1, 2]).to_numpy()

final_station_info = {}
for item in station_info:
    final_station_info[item['station_id']] = item
    final_station_info[item['station_id']]['max_capacity'] = max_capacity[item['station_id']]
    final_station_info[item['station_id']]['init_inventory'] = initial_bike[item['station_id']]
    final_station_info[item['station_id']].pop('station_id')


station_info = final_station_info