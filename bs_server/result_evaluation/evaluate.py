# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu
@license: Apache Licence 
@file: evaluate.py 
@time: 2020/10/10
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020
"""
from itertools import groupby
from geopy.distance import geodesic
from more_itertools import pairwise

from bs_server.rebalancing_preprocessing.main import current_stage
from dist_matrix import get_distance
from bs_server.confreader import read_config as cfg
from bs_server.data import *

truck_count = int(cfg('station_info', 'truck_count'))


def evaluate(x):
    routes = [list(group) for k, group in groupby(list(x), lambda y: y == -1) if not k]
    rebalancing_cost = 0
    derivation = 0
    satisfaction = 0
    station_count = 0
    routing_report = {'routes': [], 'sat_profit': 0, 'rebalancing_cost': 0, 'total_rebalancing_amount': 0}
    total_rebalancing_amount = 0
    centroid = (32.03803975535169, 118.7987139091005)
    truck_inventory_list = [30,31]
    key = [15037, 11028]
    for idx, route in enumerate(routes):
        if current_stage != 0:
            centroid_station = (key_info[key[idx]])
            centroid = (centroid_station['latitude'], centroid_station['longitude'])
        else:
            centroid = centroid
        route_info = {
            "station_list": [],
            "satisfaction_list": [],
            "arriving_time": [],
            "demand": [],
            "actual_allocation": [],
            "truck_inventory": [],
            "sat_profit": 0,
            "rebalancing_cost": 0
        }
        # route.insert(0, list(station_info.keys())[idx])
        # print(route)

        current_time = 0
        first_stop = station_info[station_list.index(route[0])]
        center_to_first = geodesic((first_stop['latitude'], first_stop['longitude']), centroid).m / truck_velocity

        current_time += center_to_first
        rebalancing_cost += center_to_first * travel_cost
        truck_inventory = truck_inventory_list[idx]
        for station, next_station in pairwise(route + [route[0]]):
            station_obj = station_info[station_list.index(station)]
            route_info['station_list'].append(station_obj['id'])
            route_info['arriving_time'].append(current_time)
            route_info['demand'].append(station_obj['demand'])
            func_2 = derivation_from_target_penalty_calculation(station_obj, current_time, truck_inventory)
            derivation += func_2[0]
            truck_inventory = func_2[1]
            route_info['truck_inventory'].append(truck_inventory)
            total_rebalancing_amount += func_2[2]
            route_info['actual_allocation'].append(func_2[2])
            satisfaction += satisfaction_calculation(station_obj, current_time, func_2[2])
            route_info['satisfaction_list'].append(satisfaction_calculation(station_obj, current_time, func_2[2]))
            travel_time_to_next = get_distance(station, next_station) / truck_velocity
            working_time = 1 / 6 * func_2[2]
            rebalancing_cost += travel_time_to_next * travel_cost + working_time * working_cost
            current_time += get_distance(station, next_station) / truck_velocity + working_time
            station_count += 1
            if current_time > 15:
                break
        routing_report['routes'].append(route_info)
        routing_report['sat_profit'] = satisfaction
        routing_report['rebalancing_cost'] = rebalancing_cost + 40 * truck_count
        routing_report['total_rebalancing_amount'] = total_rebalancing_amount
    return rebalancing_cost + 40 * truck_count, total_rebalancing_amount, satisfaction, station_count, routing_report


def satisfaction_calculation(station, arriving_time, rebalancing_amount):
    expected_time = station['full_empty_time']
    # 晚于最晚到达时间，满意度全部为0
    if arriving_time >= expected_time + reserved_time:
        return 0
    # 在下降期间到达：
    if expected_time < arriving_time < expected_time + reserved_time:
        # 降到0以前一共能调度的车辆数
        valid_amount = (expected_time + reserved_time - arriving_time) / 10 * 60
        total_sat = 0
        for i in range(1, int(min(valid_amount, rebalancing_amount)) + 1):
            total_sat += -1 / reserved_time * (arriving_time + 10 / 60 * i - expected_time - reserved_time)
        return total_sat
    # 在下降之前到达
    if arriving_time <= expected_time:
        # 开始下降前一共能调度的车辆数
        valid_amount_01 = (expected_time - arriving_time) / 10 * 60
        total_sat = min(valid_amount_01, rebalancing_amount) * 1
        valid_amount_02 = (expected_time + reserved_time - arriving_time) / 10 * 60
        if rebalancing_amount - valid_amount_01 > 0:
            for i in range(1, int(min(valid_amount_02, rebalancing_amount - valid_amount_01)) + 1):
                total_sat += -1 / reserved_time * (10 / 60 * i - reserved_time)
        return total_sat


def derivation_from_target_penalty_calculation(station, current_time, truck_inventory):
    rebalancing_amount = 0
    station_remaining_bike = min(max(station['bike_count'] - station['velocity'] * current_time, 0), station['max_capacity'])
    if station['demand'] > 0:
        rebalancing_amount = min(min(truck_inventory, station['demand']),
                                 station['max_capacity'] - station_remaining_bike)
        truck_inventory -= rebalancing_amount
    elif station['demand'] < 0:
        rebalancing_amount = min(min(-station['demand'], truck_capacity - truck_inventory), station['bike_count'])
        truck_inventory += rebalancing_amount
    return abs(abs(station['demand']) - abs(rebalancing_amount)), truck_inventory, abs(rebalancing_amount)
