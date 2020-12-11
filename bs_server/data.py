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

from bs_server.confreader import read_config as cfg

# from dist_matrix import distance_matrix

pref = None
system = 'mac'
if system == 'mac':
    pref = '~/project/bs_rebalancing_platform/'
else:
    pref = '~/'

station_count = int(cfg('station_info', 'station_count'))
truck_count = int(cfg('station_info', 'truck_count'))
truck_velocity = int(cfg('station_info', 'truck_velocity'))
travel_cost = float(cfg('station_info', 'travel_cost'))
working_cost = float(cfg('station_info', 'working_cost'))
reserved_time = int(cfg('station_info', 'reserved_time'))
truck_capacity = int(cfg('station_info', 'truck_capacity'))

"""
# 初始化数据库连接:
engine = create_engine('mysql+mysqldb://root:95930908@localhost:3306/bikeshare_docked')
# 创建DBSession类型:
Session = sessionmaker(bind=engine)


session = Session()
station_obj_list = sorted([r for r in session.query(Station)], key=lambda m: m.priority, reverse=True)[:38]
station_list = [r.id for r in station_obj_list]

print(station_list)
"""
station_list = [15067, 13094, 11024, 15031, 15077, 13097, 13017, 15075, 15029, 15056, 11127, 13025, 15088, 13095, 11102,
                11126, 11018, 15001, 11101, 15003, 11012, 15007, 13005, 15048, 13098, 15023, 15045, 15062, 11030, 15012,
                15144, 15009, 13013, 15143, 15037, 15047, 15120, 11021, 11130, 13009, 15035, 15100, 15061, 15068, 13062,
                15038, 11002, 15042, 15070, 11011, 15057, 11104, 11009, 11028, 11271, 11035]

# station_list = [15100, 11130, 15012, 15048, 15009, 15001, 13098, 11018, 15037, 15068, 15062, 15035, 13097, 13062, 15061, 15120, 11012, 15045, 15038, 13017, 11102, 13013, 15042, 15067, 11028, 15057, 15056, 11021, 11030, 15070, 13095, 11009, 11127, 11271, 11024, 11101, 11104, 11035]
# station_list = [11028, 15037, 11130, 15001, 13013, 15012, 11018, 15068, 15061, 13097, 15038, 11021, 13062, 15057, 11002, 15067, 11012, 15070, 15056, 11009, 11271]

# station_list = [15012, 15062, 15038, 15068, 13013, 11130, 15067, 13062, 11012, 15001, 13017, 15045, 15070, 15056, 11009,
#                 11018, 11101, 11271]
# station_list=

# station_info = json.dumps([o.dump_to_json() for o in station_obj_list])

# print(station_info)

"""
key_info = {
    15031: {"id": 15031, "full_empty_time": 21.21, "max_capacity": 27, "bike_count": 7, "priority": 25.31,
            "diversity": None,
            "velocity": 0.33, "latitude": 32.031, "longitude": 118.778, "demand": 19},
    15003: {"id": 15003, "full_empty_time": 43.48, "max_capacity": 58, "bike_count": 20, "priority": 19.02,
            "diversity": None,
            "velocity": 0.46, "latitude": 32.0424, "longitude": 118.777, "demand": 20},
    13025: {"id": 13025, "full_empty_time": 32.81, "max_capacity": 58, "bike_count": 21, "priority": 21.94,
            "diversity": None,
            "velocity": 0.64, "latitude": 32.0702, "longitude": 118.785, "demand": 29}
}
"""

key_info = {
    15037: {"id": 15037, "full_empty_time": 21.21, "max_capacity": 27, "bike_count": 7, "priority": 25.31,
            "diversity": None,
            "velocity": 0.33, "latitude": 32.029, "longitude": 118.792, "demand": 19},
    11028: {"id": 11028, "full_empty_time": 43.48, "max_capacity": 58, "bike_count": 20, "priority": 19.02,
            "diversity": None,
            "velocity": 0.46, "latitude": 32.0659, "longitude": 118.779, "demand": 20},

}

# key_info = {
#     15100: {"id": 15100, "full_empty_time": 21.21, "max_capacity": 27, "bike_count": 7, "priority": 25.31,
#             "diversity": None,
#             "velocity": 0.33, "latitude": 32.0355, "longitude": 118.779, "demand": 19},
#     13098: {"id": 13098, "full_empty_time": 43.48, "max_capacity": 58, "bike_count": 20, "priority": 19.02,
#             "diversity": None,
#             "velocity": 0.46, "latitude": 32.048, "longitude": 118.787, "demand": 20},
#
# }


"""
station_info = [
    {"id": 15067, "full_empty_time": 0.0, "max_capacity": 36, "bike_count": 0, "priority": 26.7, "diversity": None,
     "velocity": 0.12, "latitude": 32.014, "longitude": 118.79, "demand": 15},
    {"id": 13094, "full_empty_time": 8.33, "max_capacity": 35, "bike_count": 1, "priority": 26.23, "diversity": None,
     "velocity": 0.12, "latitude": 32.0557, "longitude": 118.796, "demand": 14},
    {"id": 11024, "full_empty_time": 10.0, "max_capacity": 47, "bike_count": 1, "priority": 25.76, "diversity": None,
     "velocity": 0.1, "latitude": 32.0641, "longitude": 118.765, "demand": 15},
    {"id": 15031, "full_empty_time": 21.21, "max_capacity": 27, "bike_count": 7, "priority": 25.31, "diversity": None,
     "velocity": 0.33, "latitude": 32.031, "longitude": 118.778, "demand": 19},
    {"id": 15077, "full_empty_time": 20.0, "max_capacity": 27, "bike_count": 2, "priority": 24.86, "diversity": None,
     "velocity": 0.1, "latitude": 32.0325, "longitude": 118.775, "demand": 10},
    {"id": 13097, "full_empty_time": 22.22, "max_capacity": 26, "bike_count": 4, "priority": 24.42, "diversity": None,
     "velocity": 0.18, "latitude": 32.0521, "longitude": 118.788, "demand": 12},
    {"id": 13017, "full_empty_time": 23.08, "max_capacity": 36, "bike_count": 3, "priority": 23.99, "diversity": None,
     "velocity": 0.13, "latitude": 32.0579, "longitude": 118.806, "demand": 12},
    {"id": 15075, "full_empty_time": 26.92, "max_capacity": 33, "bike_count": 7, "priority": 23.56, "diversity": None,
     "velocity": 0.26, "latitude": 32.033, "longitude": 118.79, "demand": 16},
    {"id": 15029, "full_empty_time": 30.38, "max_capacity": 60, "bike_count": 24, "priority": 23.15, "diversity": None,
     "velocity": 0.79, "latitude": 32.0334, "longitude": 118.792, "demand": 36},
    {"id": 15056, "full_empty_time": 28.57, "max_capacity": 45, "bike_count": 2, "priority": 22.74, "diversity": None,
     "velocity": 0.07, "latitude": 32.0193, "longitude": 118.77, "demand": 12},
    {"id": 11127, "full_empty_time": 29.41, "max_capacity": 37, "bike_count": 5, "priority": 22.34, "diversity": None,
     "velocity": 0.17, "latitude": 32.0724, "longitude": 118.773, "demand": 13},
    {"id": 13025, "full_empty_time": 32.81, "max_capacity": 58, "bike_count": 21, "priority": 21.94, "diversity": None,
     "velocity": 0.64, "latitude": 32.0702, "longitude": 118.785, "demand": 29},
    {"id": 15088, "full_empty_time": 31.25, "max_capacity": 44, "bike_count": 5, "priority": 21.55, "diversity": None,
     "velocity": 0.16, "latitude": 32.0318, "longitude": 118.773, "demand": 14},
    {"id": 13095, "full_empty_time": 33.33, "max_capacity": 22, "bike_count": 1, "priority": 21.17, "diversity": None,
     "velocity": 0.03, "latitude": 32.0648, "longitude": 118.786, "demand": 6},
    {"id": 11102, "full_empty_time": 37.66, "max_capacity": 46, "bike_count": 17, "priority": 20.8, "diversity": None,
     "velocity": -0.77, "latitude": 32.0719, "longitude": 118.778, "demand": -27},
    {"id": 11126, "full_empty_time": 37.93, "max_capacity": 29, "bike_count": 11, "priority": 20.43, "diversity": None,
     "velocity": 0.29, "latitude": 32.0578, "longitude": 118.784, "demand": 13},
    {"id": 11018, "full_empty_time": 40.0, "max_capacity": 56, "bike_count": 12, "priority": 20.07, "diversity": None,
     "velocity": 0.3, "latitude": 32.0606, "longitude": 118.763, "demand": 18},
    {"id": 15001, "full_empty_time": 41.82, "max_capacity": 52, "bike_count": 23, "priority": 19.71, "diversity": None,
     "velocity": 0.55, "latitude": 32.0426, "longitude": 118.767, "demand": 21},
    {"id": 11101, "full_empty_time": 40.0, "max_capacity": 33, "bike_count": 2, "priority": 19.36, "diversity": None,
     "velocity": 0.05, "latitude": 32.0665, "longitude": 118.767, "demand": 8},
    {"id": 15003, "full_empty_time": 43.48, "max_capacity": 58, "bike_count": 20, "priority": 19.02, "diversity": None,
     "velocity": 0.46, "latitude": 32.0424, "longitude": 118.777, "demand": 20},
    {"id": 11012, "full_empty_time": 43.86, "max_capacity": 37, "bike_count": 12, "priority": 18.68, "diversity": None,
     "velocity": -0.57, "latitude": 32.0519, "longitude": 118.771, "demand": -17},
    {"id": 15007, "full_empty_time": 45.45, "max_capacity": 58, "bike_count": 10, "priority": 18.35, "diversity": None,
     "velocity": 0.22, "latitude": 32.0414, "longitude": 118.795, "demand": 15},
    {"id": 13005, "full_empty_time": 45.45, "max_capacity": 36, "bike_count": 10, "priority": 18.03, "diversity": None,
     "velocity": 0.22, "latitude": 32.0437, "longitude": 118.795, "demand": 11},
    {"id": 15048, "full_empty_time": 45.45, "max_capacity": 35, "bike_count": 25, "priority": 17.71, "diversity": None,
     "velocity": -0.22, "latitude": 32.0229, "longitude": 118.782, "demand": -11},
    {"id": 13098, "full_empty_time": 45.45, "max_capacity": 37, "bike_count": 5, "priority": 17.39, "diversity": None,
     "velocity": 0.11, "latitude": 32.048, "longitude": 118.787, "demand": 9},
    {"id": 15023, "full_empty_time": 50.0, "max_capacity": 41, "bike_count": 6, "priority": 17.09, "diversity": None,
     "velocity": 0.12, "latitude": 32.0358, "longitude": 118.79, "demand": 10},
    {"id": 15045, "full_empty_time": 50.0, "max_capacity": 35, "bike_count": 12, "priority": 16.78, "diversity": None,
     "velocity": 0.24, "latitude": 32.0231, "longitude": 118.777, "demand": 10},
    {"id": 15062, "full_empty_time": 60.0, "max_capacity": 52, "bike_count": 3, "priority": 16.49, "diversity": None,
     "velocity": 0.05, "latitude": 32.0229, "longitude": 118.798, "demand": 11},
    {"id": 11030, "full_empty_time": 57.14, "max_capacity": 46, "bike_count": 4, "priority": 16.2, "diversity": None,
     "velocity": 0.07, "latitude": 32.064, "longitude": 118.779, "demand": 10},
    {"id": 15012, "full_empty_time": 60.0, "max_capacity": 60, "bike_count": 17, "priority": 15.91, "diversity": None,
     "velocity": 0.24, "latitude": 32.0399, "longitude": 118.784, "demand": 10},
    {"id": 15144, "full_empty_time": 60.0, "max_capacity": 30, "bike_count": 16, "priority": 15.63, "diversity": None,
     "velocity": -0.23, "latitude": 32.03, "longitude": 118.799, "demand": -6},
    {"id": 15009, "full_empty_time": 60.0, "max_capacity": 55, "bike_count": 12, "priority": 15.35, "diversity": None,
     "velocity": 0.09, "latitude": 32.0408, "longitude": 118.803, "demand": 5},
    {"id": 13013, "full_empty_time": 60.0, "max_capacity": 59, "bike_count": 14, "priority": 15.08, "diversity": None,
     "velocity": 0.16, "latitude": 32.0602, "longitude": 118.785, "demand": 8},
    {"id": 15143, "full_empty_time": 60.0, "max_capacity": 35, "bike_count": 10, "priority": 14.81, "diversity": None,
     "velocity": 0.06, "latitude": 32.0328, "longitude": 118.801, "demand": 1},
    {"id": 15037, "full_empty_time": 60.0, "max_capacity": 48, "bike_count": 17, "priority": 14.55, "diversity": None,
     "velocity": -0.42, "latitude": 32.029, "longitude": 118.792, "demand": -4},
    {"id": 15047, "full_empty_time": 60.0, "max_capacity": 41, "bike_count": 10, "priority": 14.29, "diversity": None,
     "velocity": 0.12, "latitude": 32.024, "longitude": 118.782, "demand": 6},
    {"id": 15120, "full_empty_time": 60.0, "max_capacity": 24, "bike_count": 5, "priority": 14.04, "diversity": None,
     "velocity": 0.07, "latitude": 32.0216, "longitude": 118.8, "demand": 5},
    {"id": 11021, "full_empty_time": 60.0, "max_capacity": 34, "bike_count": 12, "priority": 13.79, "diversity": None,
     "velocity": 0.2, "latitude": 32.0597, "longitude": 118.765, "demand": 7},
    {"id": 11130, "full_empty_time": 60.0, "max_capacity": 43, "bike_count": 28, "priority": 13.55, "diversity": None,
     "velocity": 0.41, "latitude": 32.0602, "longitude": 118.784, "demand": 6},
    {"id": 13009, "full_empty_time": 60.0, "max_capacity": 51, "bike_count": 11, "priority": 13.31, "diversity": None,
     "velocity": 0.02, "latitude": 32.0488, "longitude": 118.797, "demand": 1},
    {"id": 15035, "full_empty_time": 60.0, "max_capacity": 58, "bike_count": 13, "priority": 13.07, "diversity": None,
     "velocity": 0.04, "latitude": 32.0306, "longitude": 118.782, "demand": 2},
    {"id": 15100, "full_empty_time": 60.0, "max_capacity": 39, "bike_count": 12, "priority": 12.84, "diversity": None,
     "velocity": 0.1, "latitude": 32.0355, "longitude": 118.779, "demand": 2},
    {"id": 15061, "full_empty_time": 60.0, "max_capacity": 36, "bike_count": 10, "priority": 12.61, "diversity": None,
     "velocity": 0.05, "latitude": 32.0212, "longitude": 118.796, "demand": 1},
    {"id": 15068, "full_empty_time": 60.0, "max_capacity": 59, "bike_count": 28, "priority": 12.39, "diversity": None,
     "velocity": 0.33, "latitude": 32.0149, "longitude": 118.795, "demand": 4},
    {"id": 13062, "full_empty_time": 60.0, "max_capacity": 41, "bike_count": 17, "priority": 12.17, "diversity": None,
     "velocity": 0.21, "latitude": 32.0632, "longitude": 118.793, "demand": 4},
    {"id": 15038, "full_empty_time": 60.0, "max_capacity": 34, "bike_count": 12, "priority": 11.96, "diversity": None,
     "velocity": 0.11, "latitude": 32.0271, "longitude": 118.777, "demand": 2},
    {"id": 11002, "full_empty_time": 60.0, "max_capacity": 32, "bike_count": 9, "priority": 11.74, "diversity": None,
     "velocity": 0.05, "latitude": 32.0429, "longitude": 118.771, "demand": 1},
    {"id": 15042, "full_empty_time": 60.0, "max_capacity": 47, "bike_count": 11, "priority": 11.54, "diversity": None,
     "velocity": 0.05, "latitude": 32.0255, "longitude": 118.772, "demand": 2},
    {"id": 15070, "full_empty_time": 60.0, "max_capacity": 35, "bike_count": 8, "priority": 11.33, "diversity": None,
     "velocity": 0.06, "latitude": 32.009, "longitude": 118.793, "demand": 3},
    {"id": 11011, "full_empty_time": 60.0, "max_capacity": 32, "bike_count": 7, "priority": 11.13, "diversity": None,
     "velocity": 0.02, "latitude": 32.0497, "longitude": 118.77, "demand": 1},
    {"id": 15057, "full_empty_time": 60.0, "max_capacity": 45, "bike_count": 12, "priority": 10.93, "diversity": None,
     "velocity": 0.06, "latitude": 32.0189, "longitude": 118.775, "demand": 1},
    {"id": 11104, "full_empty_time": 60.0, "max_capacity": 28, "bike_count": 14, "priority": 10.74, "diversity": None,
     "velocity": 0.2, "latitude": 32.0688, "longitude": 118.765, "demand": 4},
    {"id": 11009, "full_empty_time": 60.0, "max_capacity": 29, "bike_count": 9, "priority": 10.55, "diversity": None,
     "velocity": 0.07, "latitude": 32.0513, "longitude": 118.764, "demand": 2},
    {"id": 11028, "full_empty_time": 60.0, "max_capacity": 31, "bike_count": 4, "priority": 10.36, "diversity": None,
     "velocity": -0.38, "latitude": 32.066, "longitude": 118.77, "demand": -2},
    {"id": 11271, "full_empty_time": 60.0, "max_capacity": 34, "bike_count": 8, "priority": 10.18, "diversity": None,
     "velocity": 0.02, "latitude": 32.0654, "longitude": 118.76, "demand": 1},
    {"id": 11035, "full_empty_time": 60.0, "max_capacity": 45, "bike_count": 10, "priority": 10.0, "diversity": None,
     "velocity": 0.02, "latitude": 32.0763, "longitude": 118.77, "demand": 1}]
"""

# station_info = [{"id": 15100, "full_empty_time": 0.0, "max_capacity": 39, "bike_count": 0, "priority": 26.48, "diversity": None, "velocity": 0.59, "latitude": 32.0355, "longitude": 118.779, "demand": 35}, {"id": 11130, "full_empty_time": 0.0, "max_capacity": 43, "bike_count": 0, "priority": 25.79, "diversity": None, "velocity": 0.72, "latitude": 32.0602, "longitude": 118.784, "demand": 41}, {"id": 15012, "full_empty_time": 0.0, "max_capacity": 60, "bike_count": 0, "priority": 25.12, "diversity": None, "velocity": 0.24, "latitude": 32.0399, "longitude": 118.784, "demand": 23}, {"id": 15048, "full_empty_time": 0.0, "max_capacity": 35, "bike_count": 35, "priority": 24.47, "diversity": None, "velocity": -0.46, "latitude": 32.0229, "longitude": 118.782, "demand": -28}, {"id": 15009, "full_empty_time": 0.0, "max_capacity": 55, "bike_count": 0, "priority": 23.83, "diversity": None, "velocity": 0.03, "latitude": 32.0408, "longitude": 118.803, "demand": 13}, {"id": 15001, "full_empty_time": 0.0, "max_capacity": 52, "bike_count": 0, "priority": 23.21, "diversity": None, "velocity": 0.56, "latitude": 32.0426, "longitude": 118.767, "demand": 36}, {"id": 13098, "full_empty_time": 0.0, "max_capacity": 37, "bike_count": 0, "priority": 22.61, "diversity": None, "velocity": 0.23, "latitude": 32.048, "longitude": 118.787, "demand": 18}, {"id": 11018, "full_empty_time": 0.0, "max_capacity": 56, "bike_count": 0, "priority": 22.02, "diversity": None, "velocity": 0.84, "latitude": 32.0606, "longitude": 118.763, "demand": 49}, {"id": 15037, "full_empty_time": 0.0, "max_capacity": 48, "bike_count": 48, "priority": 21.45, "diversity": None, "velocity": -0.07, "latitude": 32.029, "longitude": 118.792, "demand": -13}, {"id": 15068, "full_empty_time": 0.0, "max_capacity": 59, "bike_count": 0, "priority": 20.89, "diversity": None, "velocity": 0.3, "latitude": 32.0149, "longitude": 118.795, "demand": 26}, {"id": 15062, "full_empty_time": 0.0, "max_capacity": 52, "bike_count": 0, "priority": 20.35, "diversity": None, "velocity": 0.06, "latitude": 32.0229, "longitude": 118.798, "demand": 14}, {"id": 15035, "full_empty_time": 0.0, "max_capacity": 58, "bike_count": 0, "priority": 19.82, "diversity": None, "velocity": 0.07, "latitude": 32.0306, "longitude": 118.782, "demand": 15}, {"id": 13097, "full_empty_time": 0.0, "max_capacity": 26, "bike_count": 0, "priority": 19.31, "diversity": None, "velocity": 0.17, "latitude": 32.0521, "longitude": 118.788, "demand": 13}, {"id": 13062, "full_empty_time": 0.0, "max_capacity": 41, "bike_count": 0, "priority": 18.81, "diversity": None, "velocity": 0.32, "latitude": 32.0632, "longitude": 118.793, "demand": 23}, {"id": 15061, "full_empty_time": 0.0, "max_capacity": 36, "bike_count": 0, "priority": 18.32, "diversity": None, "velocity": 0.09, "latitude": 32.0212, "longitude": 118.796, "demand": 12}, {"id": 15120, "full_empty_time": 0.0, "max_capacity": 24, "bike_count": 0, "priority": 17.84, "diversity": None, "velocity": 0.11, "latitude": 32.0216, "longitude": 118.8, "demand": 10}, {"id": 11012, "full_empty_time": 0.0, "max_capacity": 37, "bike_count": 37, "priority": 17.38, "diversity": None, "velocity": -0.34, "latitude": 32.0519, "longitude": 118.771, "demand": -23}, {"id": 15045, "full_empty_time": 0.0, "max_capacity": 35, "bike_count": 0, "priority": 16.93, "diversity": None, "velocity": 0.24, "latitude": 32.0231, "longitude": 118.777, "demand": 18}, {"id": 15038, "full_empty_time": 0.0, "max_capacity": 34, "bike_count": 0, "priority": 16.49, "diversity": None, "velocity": 0.16, "latitude": 32.0271, "longitude": 118.777, "demand": 14}, {"id": 13017, "full_empty_time": 0.0, "max_capacity": 36, "bike_count": 0, "priority": 16.06, "diversity": None, "velocity": 0.12, "latitude": 32.0579, "longitude": 118.806, "demand": 13}, {"id": 11102, "full_empty_time": 0.0, "max_capacity": 46, "bike_count": 46, "priority": 15.64, "diversity": None, "velocity": -0.51, "latitude": 32.0719, "longitude": 118.778, "demand": -33}, {"id": 13013, "full_empty_time": 0.0, "max_capacity": 59, "bike_count": 0, "priority": 15.24, "diversity": None, "velocity": 0.1, "latitude": 32.0602, "longitude": 118.785, "demand": 17}, {"id": 15042, "full_empty_time": 0.0, "max_capacity": 47, "bike_count": 0, "priority": 14.84, "diversity": None, "velocity": 0.18, "latitude": 32.0255, "longitude": 118.772, "demand": 18}, {"id": 15067, "full_empty_time": 0.0, "max_capacity": 36, "bike_count": 0, "priority": 14.45, "diversity": None, "velocity": 0.1, "latitude": 32.014, "longitude": 118.79, "demand": 12}, {"id": 11028, "full_empty_time": 0.0, "max_capacity": 31, "bike_count": 31, "priority": 14.08, "diversity": None, "velocity": -0.44, "latitude": 32.066, "longitude": 118.77, "demand": -26}, {"id": 15057, "full_empty_time": 0.0, "max_capacity": 45, "bike_count": 0, "priority": 13.71, "diversity": None, "velocity": 0.12, "latitude": 32.0189, "longitude": 118.775, "demand": 15}, {"id": 15056, "full_empty_time": 0.0, "max_capacity": 45, "bike_count": 0, "priority": 13.36, "diversity": None, "velocity": 0.19, "latitude": 32.0193, "longitude": 118.77, "demand": 18}, {"id": 11021, "full_empty_time": 0.0, "max_capacity": 34, "bike_count": 0, "priority": 13.01, "diversity": None, "velocity": 0.32, "latitude": 32.0597, "longitude": 118.765, "demand": 22}, {"id": 11030, "full_empty_time": 0.0, "max_capacity": 46, "bike_count": 0, "priority": 12.67, "diversity": None, "velocity": 0.13, "latitude": 32.064, "longitude": 118.779, "demand": 16}, {"id": 15070, "full_empty_time": 0.0, "max_capacity": 35, "bike_count": 0, "priority": 12.34, "diversity": None, "velocity": 0.11, "latitude": 32.009, "longitude": 118.793, "demand": 12}, {"id": 13095, "full_empty_time": 0.0, "max_capacity": 22, "bike_count": 22, "priority": 12.02, "diversity": None, "velocity": -0.1, "latitude": 32.0648, "longitude": 118.786, "demand": -9}, {"id": 11009, "full_empty_time": 0.0, "max_capacity": 29, "bike_count": 0, "priority": 11.71, "diversity": None, "velocity": 0.18, "latitude": 32.0513, "longitude": 118.764, "demand": 14}, {"id": 11127, "full_empty_time": 0.0, "max_capacity": 37, "bike_count": 0, "priority": 11.41, "diversity": None, "velocity": 0.11, "latitude": 32.0724, "longitude": 118.773, "demand": 13}, {"id": 11271, "full_empty_time": 0.0, "max_capacity": 34, "bike_count": 0, "priority": 11.11, "diversity": None, "velocity": 0.16, "latitude": 32.0654, "longitude": 118.76, "demand": 14}, {"id": 11024, "full_empty_time": 0.0, "max_capacity": 47, "bike_count": 0, "priority": 10.82, "diversity": None, "velocity": 0.03, "latitude": 32.0641, "longitude": 118.765, "demand": 11}, {"id": 11101, "full_empty_time": 0.0, "max_capacity": 33, "bike_count": 0, "priority": 10.54, "diversity": None, "velocity": 0.02, "latitude": 32.0665, "longitude": 118.767, "demand": 8}, {"id": 11104, "full_empty_time": 45.0, "max_capacity": 28, "bike_count": 14, "priority": 10.27, "diversity": None, "velocity": -0.3, "latitude": 32.0688, "longitude": 118.765, "demand": -6}, {"id": 11035, "full_empty_time": 45.0, "max_capacity": 45, "bike_count": 10, "priority": 10.0, "diversity": None, "velocity": 0.03, "latitude": 32.0763, "longitude": 118.77, "demand": 1}]


# station_info = [{"id": 11028, "full_empty_time": 0.0, "max_capacity": 31, "bike_count": 31, "priority": 25.92, "diversity": None, "velocity": -1.68, "latitude": 32.066, "longitude": 118.77, "demand": -57}, {"id": 15037, "full_empty_time": 0.0, "max_capacity": 48, "bike_count": 48, "priority": 24.71, "diversity": None, "velocity": -0.68, "latitude": 32.029, "longitude": 118.792, "demand": -30}, {"id": 11130, "full_empty_time": 0.0, "max_capacity": 43, "bike_count": 0, "priority": 23.56, "diversity": None, "velocity": 0.63, "latitude": 32.0602, "longitude": 118.784, "demand": 28}, {"id": 15001, "full_empty_time": 0.0, "max_capacity": 52, "bike_count": 0, "priority": 22.47, "diversity": None, "velocity": 0.6, "latitude": 32.0426, "longitude": 118.767, "demand": 29}, {"id": 13013, "full_empty_time": 0.0, "max_capacity": 59, "bike_count": 0, "priority": 21.42, "diversity": None, "velocity": 0.48, "latitude": 32.0602, "longitude": 118.785, "demand": 27}, {"id": 15012, "full_empty_time": 0.0, "max_capacity": 60, "bike_count": 0, "priority": 20.43, "diversity": None, "velocity": 0.2, "latitude": 32.0399, "longitude": 118.784, "demand": 18}, {"id": 11018, "full_empty_time": 0.0, "max_capacity": 56, "bike_count": 0, "priority": 19.48, "diversity": None, "velocity": 0.6, "latitude": 32.0606, "longitude": 118.763, "demand": 30}, {"id": 15068, "full_empty_time": 0.0, "max_capacity": 59, "bike_count": 0, "priority": 18.57, "diversity": None, "velocity": 0.17, "latitude": 32.0149, "longitude": 118.795, "demand": 17}, {"id": 15061, "full_empty_time": 0.0, "max_capacity": 36, "bike_count": 0, "priority": 17.71, "diversity": None, "velocity": 0.07, "latitude": 32.0212, "longitude": 118.796, "demand": 10}, {"id": 13097, "full_empty_time": 0.0, "max_capacity": 26, "bike_count": 0, "priority": 16.88, "diversity": None, "velocity": 0.02, "latitude": 32.0521, "longitude": 118.788, "demand": 6}, {"id": 15038, "full_empty_time": 0.0, "max_capacity": 34, "bike_count": 0, "priority": 16.1, "diversity": None, "velocity": 0.13, "latitude": 32.0271, "longitude": 118.777, "demand": 11}, {"id": 11021, "full_empty_time": 0.0, "max_capacity": 34, "bike_count": 0, "priority": 15.35, "diversity": None, "velocity": 0.45, "latitude": 32.0597, "longitude": 118.765, "demand": 21}, {"id": 13062, "full_empty_time": 0.0, "max_capacity": 41, "bike_count": 0, "priority": 14.64, "diversity": None, "velocity": 0.12, "latitude": 32.0632, "longitude": 118.793, "demand": 12}, {"id": 15057, "full_empty_time": 0.0, "max_capacity": 45, "bike_count": 0, "priority": 13.96, "diversity": None, "velocity": 0.15, "latitude": 32.0189, "longitude": 118.775, "demand": 14}, {"id": 11002, "full_empty_time": 8.33, "max_capacity": 32, "bike_count": 31, "priority": 13.31, "diversity": None, "velocity": -0.12, "latitude": 32.0429, "longitude": 118.771, "demand": -9}, {"id": 15067, "full_empty_time": 0.0, "max_capacity": 36, "bike_count": 0, "priority": 12.69, "diversity": None, "velocity": 0.05, "latitude": 32.014, "longitude": 118.79, "demand": 9}, {"id": 11012, "full_empty_time": 0.0, "max_capacity": 37, "bike_count": 37, "priority": 12.1, "diversity": None, "velocity": -0.1, "latitude": 32.0519, "longitude": 118.771, "demand": -11}, {"id": 15070, "full_empty_time": 0.0, "max_capacity": 35, "bike_count": 0, "priority": 11.54, "diversity": None, "velocity": 0.13, "latitude": 32.009, "longitude": 118.793, "demand": 11}, {"id": 15056, "full_empty_time": 0.0, "max_capacity": 45, "bike_count": 0, "priority": 11.0, "diversity": None, "velocity": 0.03, "latitude": 32.0193, "longitude": 118.77, "demand": 10}, {"id": 11009, "full_empty_time": 0.0, "max_capacity": 29, "bike_count": 0, "priority": 10.49, "diversity": None, "velocity": 0.08, "latitude": 32.0513, "longitude": 118.764, "demand": 9}, {"id": 11271, "full_empty_time": 0.0, "max_capacity": 34, "bike_count": 0, "priority": 10.0, "diversity": None, "velocity": 0.08, "latitude": 32.0654, "longitude": 118.76, "demand": 10}]
# print(station_info)

station_info = [
    {"id": 15012, "full_empty_time": 0.0, "max_capacity": 60, "bike_count": 0, "priority": 25.71, "diversity": None,
     "velocity": 0.53, "latitude": 32.0399, "longitude": 118.784, "demand": 20},
    {"id": 15062, "full_empty_time": 10.0, "max_capacity": 52, "bike_count": 1, "priority": 24.32, "diversity": None,
     "velocity": 0.1, "latitude": 32.0229, "longitude": 118.798, "demand": 11},
    {"id": 15038, "full_empty_time": 0.0, "max_capacity": 34, "bike_count": 0, "priority": 23.01, "diversity": None,
     "velocity": 0.03, "latitude": 32.0271, "longitude": 118.777, "demand": 8},
    {"id": 15068, "full_empty_time": 0.0, "max_capacity": 59, "bike_count": 0, "priority": 21.77, "diversity": None,
     "velocity": 0.23, "latitude": 32.0149, "longitude": 118.795, "demand": 16},
    {"id": 13013, "full_empty_time": 0.0, "max_capacity": 59, "bike_count": 0, "priority": 20.59, "diversity": None,
     "velocity": 0.03, "latitude": 32.0602, "longitude": 118.785, "demand": 13},
    {"id": 11130, "full_empty_time": 0.0, "max_capacity": 43, "bike_count": 0, "priority": 19.48, "diversity": None,
     "velocity": 0.17, "latitude": 32.0602, "longitude": 118.784, "demand": 12},
    {"id": 15067, "full_empty_time": 0.0, "max_capacity": 36, "bike_count": 0, "priority": 18.42, "diversity": None,
     "velocity": 0.07, "latitude": 32.014, "longitude": 118.79, "demand": 9},
    {"id": 13062, "full_empty_time": 0.0, "max_capacity": 41, "bike_count": 0, "priority": 17.43, "diversity": None,
     "velocity": 0.13, "latitude": 32.0632, "longitude": 118.793, "demand": 11},
    {"id": 11012, "full_empty_time": 0.0, "max_capacity": 37, "bike_count": 37, "priority": 16.49, "diversity": None,
     "velocity": -0.77, "latitude": 32.0519, "longitude": 118.771, "demand": -19},
    {"id": 15001, "full_empty_time": 0.0, "max_capacity": 52, "bike_count": 0, "priority": 15.6, "diversity": None,
     "velocity": 0.4, "latitude": 32.0426, "longitude": 118.767, "demand": 17},
    {"id": 13017, "full_empty_time": 14.29, "max_capacity": 36, "bike_count": 1, "priority": 14.75, "diversity": None,
     "velocity": 0.07, "latitude": 32.0579, "longitude": 118.806, "demand": 8},
    {"id": 15045, "full_empty_time": 10.0, "max_capacity": 35, "bike_count": 2, "priority": 13.96, "diversity": None,
     "velocity": 0.2, "latitude": 32.0231, "longitude": 118.777, "demand": 8},
    {"id": 15070, "full_empty_time": 0.0, "max_capacity": 35, "bike_count": 0, "priority": 13.2, "diversity": None,
     "velocity": 0.07, "latitude": 32.009, "longitude": 118.793, "demand": 9},
    {"id": 15056, "full_empty_time": 0.0, "max_capacity": 45, "bike_count": 0, "priority": 12.49, "diversity": None,
     "velocity": 0.03, "latitude": 32.0193, "longitude": 118.77, "demand": 10},
    {"id": 11009, "full_empty_time": 0.0, "max_capacity": 29, "bike_count": 0, "priority": 11.81, "diversity": None,
     "velocity": 0.07, "latitude": 32.0513, "longitude": 118.764, "demand": 7},
    {"id": 11018, "full_empty_time": 0.0, "max_capacity": 56, "bike_count": 0, "priority": 11.18, "diversity": None,
     "velocity": 0.27, "latitude": 32.0606, "longitude": 118.763, "demand": 16},
    {"id": 11101, "full_empty_time": 0.0, "max_capacity": 33, "bike_count": 0, "priority": 10.57, "diversity": None,
     "velocity": 0.07, "latitude": 32.0665, "longitude": 118.767, "demand": 8},
    {"id": 11271, "full_empty_time": 0.0, "max_capacity": 34, "bike_count": 0, "priority": 10.0, "diversity": None,
     "velocity": 0.03, "latitude": 32.0654, "longitude": 118.76, "demand": 8}]

"""
rebalanced_info = {
    "routes": [
        {
            "station_list": [
                15007,
                15023,
                15088,
                15031
            ],
            "satisfaction_list": [
                15,
                10,
                14,
                19
            ],
            "arriving_time": [
                1.2184557043717683,
                5.660616624371769,
                11.249690891038435,
                14.760857848895578
            ],
            "demand": [
                15,
                10,
                14,
                19
            ],
            "actual_allocation": [
                15,
                10,
                14,
                19
            ],
            "truck_inventory": [
                45,
                35,
                21,
                2
            ],
            "sat_profit": 0,
            "rebalancing_cost": 0
        },
        {
            "station_list": [
                15029,
                15075,
                15003
            ],
            "satisfaction_list": [
                36,
                16,
                8
            ],
            "arriving_time": [
                1.9443432630868172,
                8.444537698801103,
                14.961815153563007
            ],
            "demand": [
                36,
                16,
                20
            ],
            "actual_allocation": [
                36,
                16,
                8
            ],
            "truck_inventory": [
                24,
                8,
                0
            ],
            "sat_profit": 0,
            "rebalancing_cost": 0
        },
        {
            "station_list": [
                13005,
                11126,
                13025
            ],
            "satisfaction_list": [
                11,
                13,
                29
            ],
            "arriving_time": [
                1.711959424234007,
                7.9381248385197205,
                13.392215426614959
            ],
            "demand": [
                11,
                13,
                29
            ],
            "actual_allocation": [
                11,
                13,
                29
            ],
            "truck_inventory": [
                49,
                36,
                7
            ],
            "sat_profit": 0,
            "rebalancing_cost": 0
        }
    ],
    "sat_profit": 171,
    "rebalancing_cost": 152.2740976119109,
    "total_rebalancing_amount": 171
}
"""

"""
rebalanced_info = {
    "routes": [
        {
            "station_list": [
                15048,
                15042,
                15100
            ],
            "satisfaction_list": [
                25,
                13,
                14
            ],
            "arriving_time": [
                2.3200783777649994,
                8.75330587466976,
                13.949449812764998
            ],
            "demand": [
                -25,
                13,
                25
            ],
            "actual_allocation": [
                25,
                13,
                14
            ],
            "truck_inventory": [
                27,
                14,
                0
            ],
            "sat_profit": 0,
            "rebalancing_cost": 0
        },
        {
            "station_list": [
                11102,
                11030,
                13098
            ],
            "satisfaction_list": [
                24,
                14,
                14
            ],
            "arriving_time": [
                1.6364253966664544,
                7.73431489738074,
                14.705198223571216
            ],
            "demand": [
                -24,
                14,
                14
            ],
            "actual_allocation": [
                24,
                14,
                14
            ],
            "truck_inventory": [
                31,
                17,
                3
            ],
            "sat_profit": 0,
            "rebalancing_cost": 0
        }
    ],
    "sat_profit": 104,
    "rebalancing_cost": 101.75753078159454,
    "total_rebalancing_amount": 104
}
"""

rebalanced_info = {
    "routes": [
        {
            "station_list": [
                15037
            ],
            "satisfaction_list": [
                12.07940676600835
            ],
            "arriving_time": [
                3.390197744663883
            ],
            "demand": [
                -30
            ],
            "actual_allocation": [
                30
            ],
            "truck_inventory": [
                30
            ],
            "sat_profit": 0,
            "rebalancing_cost": 0
        },
        {
            "station_list": [
                13097,
                11028
            ],
            "satisfaction_list": [
                2.5683249575848883,
                2.518547229885795
            ],
            "arriving_time": [
                1.10558347471704,
                7.018501629478944
            ],
            "demand": [
                6,
                -57
            ],
            "actual_allocation": [
                3,
                31
            ],
            "truck_inventory": [
                0,
                31
            ],
            "sat_profit": 0,
            "rebalancing_cost": 0
        }
    ],
    "sat_profit": 17.166278953479033,
    "rebalancing_cost": 95.60095915280665,
    "total_rebalancing_amount": 64
}

visited = []

# visited = [15007, 15023, 15088, 15031, 13005,
#            11126, 13025, 15029, 15075, 15003,
#            15048, 15042, 15100, 11102, 11030,
#            15037, 13097, 11028, 13098]
