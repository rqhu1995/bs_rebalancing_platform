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

from confreader import read_config as cfg
from data import *

truck_count = int(cfg('station_info', 'truck_count'))


def evaluate(x):
    routes = [list(group) for k, group in groupby(list(x), lambda y: y == -1) if not k]
    rebalancing_cost = 0
    derivation = 0
    satisfaction = 0
    station_count = 0
    routing_report = {'routes': [], 'sat_profit':0 , 'rebalancing_cost':0, 'total_rebalancing_amount':0}
    total_rebalancing_amount = 0
    station_list = list(station_info.keys())[4:]
    for idx, route in enumerate(routes):
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
        route.insert(0, list(station_info.keys())[idx])
        # print(route)
        current_time = 0
        center_to_first = geodesic((lat_lon[route[0]][1], lat_lon[route[0]][0]),
                                   center).km / truck_velocity
        current_time += center_to_first
        rebalancing_cost += center_to_first * travel_cost
        truck_inventory = 60
        for station, next_station in pairwise(route + [route[0]]):
            route_info['station_list'].append(station)
            route_info['arriving_time'].append(current_time)
            route_info['demand'].append(station_info[station]['demand'])
            func_2 = derivation_from_target_penalty_calculation(station, truck_inventory)
            derivation += func_2[0]
            truck_inventory = func_2[1]
            route_info['truck_inventory'].append(truck_inventory)
            total_rebalancing_amount += func_2[2]
            route_info['actual_allocation'].append(func_2[2])
            satisfaction += satisfaction_calculation(station, current_time, func_2[2])
            route_info['satisfaction_list'].append(satisfaction_calculation(station, current_time, func_2[2]))
            travel_time_to_next = distance_matrix[station, next_station] / truck_velocity
            working_time = 1 / 6 * func_2[2]
            rebalancing_cost += travel_time_to_next * travel_cost + working_time * working_cost
            current_time += distance_matrix[station, next_station] / truck_velocity + working_time
            station_count += 1
            if current_time > 15:
                break
        routing_report['routes'].append(route_info)
        routing_report['sat_profit'] = satisfaction
        routing_report['rebalancing_cost'] = rebalancing_cost + 40 * truck_count
        routing_report['total_rebalancing_amount'] = total_rebalancing_amount
    return rebalancing_cost + 40 * truck_count, total_rebalancing_amount, satisfaction, station_count, routing_report


def satisfaction_calculation(station, arriving_time, rebalancing_amount):
    expected_time = station_info[station]['full_empty_time']
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
        # print(arriving_time, expected_time)
        valid_amount_01 = (expected_time - arriving_time) / 10 * 60
        total_sat = min(valid_amount_01, rebalancing_amount) * 1
        valid_amount_02 = (expected_time + reserved_time - arriving_time) / 10 * 60
        if rebalancing_amount - valid_amount_01 > 0:
            for i in range(1, int(min(valid_amount_02, rebalancing_amount - valid_amount_01)) + 1):
                total_sat += -1 / reserved_time * (10 / 60 * i - reserved_time)
        return total_sat


def derivation_from_target_penalty_calculation(station, truck_inventory):
    station_demand = station_info[station]['demand']
    rebalancing_amount = 0
    cmax = station_info[station]['max_capacity']
    init_inventory = station_info[station]['init_inventory']
    if station_demand > 0:
        rebalancing_amount = min(min(truck_inventory, station_demand), cmax - init_inventory)
        truck_inventory -= rebalancing_amount
    elif station_demand < 0:
        rebalancing_amount = min(min(-station_demand, truck_capacity - truck_inventory), init_inventory)
        truck_inventory += rebalancing_amount
    return abs(abs(station_demand) - abs(rebalancing_amount)), truck_inventory, abs(rebalancing_amount)
