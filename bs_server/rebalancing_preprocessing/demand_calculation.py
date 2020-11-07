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

import numpy as np
from geopy.distance import geodesic
from shapely.geometry import Polygon

from bs_server.data_dockless import *


def calculate_rent_return_velocity(station,
                                   stage,
                                   delta=15,
                                   tau=60,
                                   lambda_weight=0.5):
    """
    :param stage: 当前滚动时段
    :param station: 站点对象
    :param past_rent: 历史借车值
    :param past_return: 历史还车值
    :param pred_rent: 预测借车值
    :param pred_return: 预测还车值
    :param delta: 历史考虑的时长
    :param tau: 未来预测考虑的时长
    :param lambda_weight: 加权系数
    :return:
    """

    past_rent_list = [station.past_rent_01, station.past_rent_02, station.past_rent_03, station.past_rent_04]
    past_return_list = [station.past_return_01, station.past_return_02, station.past_return_03, station.past_return_04]
    pred_rent_list = [station.pred_rent_01, station.pred_rent_02, station.pred_rent_03, station.pred_rent_04]
    pred_return_list = [station.pred_return_01, station.pred_return_02, station.pred_return_03, station.pred_return_04]

    # 前\delta分钟，后\tau分钟
    rent_return_past_velocity = (past_rent_list[stage] - past_return_list[stage]) / delta
    rent_return_pred_velocity = (pred_rent_list[stage] - pred_return_list[stage]) / tau
    velocity = rent_return_past_velocity * lambda_weight + rent_return_pred_velocity * (1 - lambda_weight)
    station.velocity = round(velocity, 2)


def calculate_warning_time(station, rent_return_velocity, remaining_time):
    """
    计算站点预警时间（2-8的时间）
    :return:
    """
    # remaining_time = initial_bike
    # 如果已经超出28，直接为0
    if (station.bike_count >= 0.8 * station.max_capacity and not (
            0.2 * station.max_capacity <= station.bike_count - rent_return_velocity * remaining_time <= 0.8 * station.max_capacity)) or (
            station.bike_count <= 0.2 * station.max_capacity and not (
            0.2 * station.max_capacity <= station.bike_count - rent_return_velocity * remaining_time <= 0.8 * station.max_capacity)):
        station.warning_time = 0

    # 否则时间是28的差值/当前速度
    elif station.bike_count > 0.2 * station.max_capacity and rent_return_velocity > 0:
        station.warning_time = round(min((station.bike_count - 0.2 * station.max_capacity) / \
                                         rent_return_velocity, remaining_time), 2)
    elif station.bike_count < 0.8 * station.max_capacity and rent_return_velocity < 0:
        station.warning_time = round(min((station.bike_count - 0.8 * station.max_capacity) / \
                                         rent_return_velocity, remaining_time), 2)

    elif rent_return_velocity == 0:
        station.warning_time = remaining_time


def calculate_full_empty_time(station, rent_return_velocity, remaining_time):
    """
    :param station:
    :param rent_return_velocity:
    :param remaining_time:
    :return:
    """
    if rent_return_velocity > 0:
        station.full_empty_time = round(min(remaining_time, station.bike_count / rent_return_velocity), 2)
    elif rent_return_velocity < 0:
        station.full_empty_time = round(
            min(remaining_time,
                (station.max_capacity - min(station.bike_count, station.max_capacity)) / (-rent_return_velocity)), 2)
    else:
        if station.bike_count == 0 or station.bike_count >= station.max_capacity:
            station.full_empty_time = 0
        else:
            station.full_empty_time = remaining_time


def calculate_demand(station, remaining_time, rent_return_velocity):
    remaining_bike = station.bike_count - rent_return_velocity * remaining_time
    if (remaining_bike <= 0) or (0 < remaining_bike < 0.2 * station.max_capacity < station.bike_count):
        station.demand = 0.2 * station.max_capacity - remaining_bike
    elif (remaining_bike > station.max_capacity) or \
            (0 < station.bike_count < 0.8 * station.max_capacity < remaining_bike < station.max_capacity) or \
            (0.8 * station.max_capacity < remaining_bike < station.max_capacity < station.bike_count):
        station.demand = -(remaining_bike - 0.8 * station.max_capacity)
    else:
        station.demand = 0

    if station.demand > 0:
        station.demand = np.ceil(station.demand).astype(int)
    else:
        station.demand = np.floor(station.demand).astype(int)


def calculate_distance(station_data, selected_cluster):
    cord_list = []
    for station in station_data:
        cord_list.append([lat_lon[station['id']][1],
                          lat_lon[station['id']][0]])
    polygon = Polygon(cord_list)
    center = polygon.centroid.coords[0]
    for station in station_data:
        station['distance'] = round(geodesic((lat_lon[station['id']][1],
                                              lat_lon[station['id']][0]),
                                             center).km, 2)
