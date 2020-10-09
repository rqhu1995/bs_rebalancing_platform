# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu
@license: Apache Licence 
@file: demand_calculation.py 
@time: 2020/10/08
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020
"""

from geopy.distance import geodesic

from bs_server.data import *


def calculate_rent_return_velocity(past_rent,
                                   past_return,
                                   pred_rent,
                                   pred_return,
                                   delta=15,
                                   tau=60,
                                   lambda_weight=0.5):
    """
    :param past_rent: 历史借车值
    :param past_return: 历史还车值
    :param pred_rent: 预测借车值
    :param pred_return: 预测还车值
    :param delta: 历史考虑的时长
    :param tau: 未来预测考虑的时长
    :param lambda_weight: 加权系数
    :return:
    """

    # 前\delta分钟，后\tau分钟
    rent_return_past_velocity = (past_rent - past_return) / delta
    rent_return_pred_velocity = (pred_rent - pred_return) / tau
    velocity = rent_return_past_velocity * lambda_weight + rent_return_pred_velocity * (1 - lambda_weight)
    return velocity


def calculate_warning_time(station, rent_return_velocity, remaining_time):
    """
    计算站点预警时间（2-8的时间）
    :return:
    """
    # 如果已经超出28，直接为0
    if initial_bike[station.station_id] >= 0.8 * max_capacity[station.station_id] or \
            initial_bike[station.station_id] <= 0.2 * max_capacity[station.station_id]:
        station.warning_time = 0
    # 否则时间是28的差值/当前速度
    elif initial_bike[station.station_id] > 0.2 * max_capacity[station.station_id] and rent_return_velocity[
        station.station_id] > 0:
        station.warning_time = round(min((initial_bike[station.station_id] - 0.2 * max_capacity[station.station_id]) / \
                                         rent_return_velocity[station.station_id], remaining_time), 2)
    elif initial_bike[station.station_id] < 0.8 * max_capacity[station.station_id] and rent_return_velocity[
        station.station_id] < 0:
        station.warning_time = round(min((initial_bike[station.station_id] - 0.8 * max_capacity[station.station_id]) / \
                                         rent_return_velocity[station.station_id], remaining_time), 2)
    elif rent_return_velocity[station.station_id] == 0:
        station.warning_time = remaining_time


def calculate_full_empty_time(station, rent_return_velocity, remaining_time):
    """
    :param station:
    :param rent_return_velocity:
    :param remaining_time:
    :return:
    """
    # 如果已经空满，直接为0
    if initial_bike[station.station_id] >= max_capacity[station.station_id] or \
            initial_bike[station.station_id] <= 0:
        station.full_empty_time = 0
    # 否则时间是和空满的差值/当前速度
    elif initial_bike[station.station_id] > 0 and rent_return_velocity[station.station_id] > 0:
        station.full_empty_time = round(
            min((initial_bike[station.station_id]) / rent_return_velocity[station.station_id],
                remaining_time), 2)
    elif initial_bike[station.station_id] < max_capacity[station.station_id] and rent_return_velocity[
        station.station_id] < 0:
        station.full_empty_time = round(min(
            (initial_bike[station.station_id] - max_capacity[station.station_id]) / rent_return_velocity[
                station.station_id],
            remaining_time), 2)
    elif rent_return_velocity[station.station_id] == 0:
        station.full_empty_time = remaining_time


def calculate_demand(station, remaining_time, rent_return_velocity):
    if station.warning_time >= remaining_time:
        station.demand = 0
    elif rent_return_velocity[station.station_id] > 0:
        station.demand = rent_return_velocity[station.station_id] * remaining_time - \
                         initial_bike[station.station_id] + 0.2 * max_capacity[station.station_id]
    elif rent_return_velocity[station.station_id] < 0:
        station.demand = rent_return_velocity[station.station_id] * remaining_time - \
                         initial_bike[station.station_id] + 0.8 * max_capacity[station.station_id]
    elif rent_return_velocity[station.station_id] == 0:
        if initial_bike[station.station_id] > 0.8 * max_capacity[station.station_id]:
            station.demand = 0.8 * max_capacity[station.station_id] - initial_bike[station.station_id]
        elif initial_bike[station.station_id] < 0.2 * max_capacity[station.station_id]:
            station.demand = 0.2 * max_capacity[station.station_id] - initial_bike[station.station_id]
    if station.demand > 0:
        station.demand = np.ceil(station.demand).astype(int)
    else:
        station.demand = np.floor(station.demand).astype(int)


def calculate_distance(station_data, selected_cluster):
    center = [
        (118.7931074, 32.04722081),
        (118.7860483, 32.02286646),
        (118.7721501, 32.06339912),
        (118.7752358, 32.04127961)
    ]
    for station_info in station_data:
        print((lat_lon[station_info['station_id']][1],
                        lat_lon[station_info['station_id']][0]),
                       (center[selected_cluster - 1][1],
                        center[selected_cluster - 1][0]))
        station_info['distance'] = round(geodesic((lat_lon[station_info['station_id']][1],
                                                 lat_lon[station_info['station_id']][0]),
                                                (center[selected_cluster - 1][1],
                                                 center[selected_cluster - 1][0])).km, 2)
