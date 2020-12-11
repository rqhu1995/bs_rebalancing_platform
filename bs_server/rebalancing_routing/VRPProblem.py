# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu
@license: Apache Licence 
@file: VRPProblem.py 
@time: 2020/10/04
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020

"""

from itertools import groupby

import numpy as np
from geopy.distance import geodesic
from more_itertools import pairwise
from pymoo.model.problem import Problem

from bs_server.data import *
from bs_server.rebalancing_preprocessing.main import current_stage
from dist_matrix import get_distance


class BSRebalancing(Problem):

    def __init__(self, **kwargs):
        super().__init__(n_var=station_count + truck_count - 1,
                         n_obj=2,
                         n_constr=0,
                         type_var=np.int,
                         **kwargs)
        self.xl = np.zeros(self.n_var)
        self.xu = np.array([[self.n_var - 1] * self.n_var])

    # 输入：随机生成的0-N排列
    def _evaluate(self, x, out, *args, **kwargs):
        # print(x)
        # session = Session()
        result = None
        # 将站点下标映射到站点编号/卡车分割
        single_route = x.copy()
        for row in range(x.shape[0]):
            for col in range(x.shape[1]):
                single_route[row, col] = station_list[x[row, col]] if x[row, col] < station_count else -1
        # 路线(解)的数量
        for cnt in range(x.shape[0]):
            real_route = list(single_route[cnt, :])
            # 一条路径编码分割为多个路线
            routes = [list(group) for k, group in groupby(real_route, lambda y: y == -1) if not k]
            sat_profit = 0
            running_cost = 0
            key = [15037, 11028]
            truck_inventory_list = [30, 31]
            centroid = (32.03803975535169, 118.7987139091005)
            for idx, route in enumerate(routes):
                # 当前时间
                # route.insert(0, list(station_info.keys())[idx])
                if current_stage != 0:
                    centroid_station = (key_info[key[idx]])
                    centroid = (centroid_station['latitude'], centroid_station['longitude'])
                else:
                    centroid = centroid
                current_time = 0
                # 车场抵达第一站
                first_stop = station_info[station_list.index(route[0])]
                center_to_first = geodesic((first_stop['latitude'], first_stop['longitude']),
                                           centroid).m / truck_velocity
                current_time += center_to_first
                running_cost += center_to_first * travel_cost
                truck_inventory = truck_inventory_list[idx]
                for station, next_station in pairwise(route + [route[0]]):
                    station_obj = station_info[station_list.index(station)]
                    func_2 = self.derivation_from_target_penalty_calculation(station_obj, current_time, truck_inventory)
                    sat_profit -= 1 * self.satisfaction_calculation(station_obj, current_time, func_2[2])
                    truck_inventory = func_2[1]
                    travel_time_to_next = get_distance(station, next_station) / truck_velocity
                    working_time = func_2[2] * 1 / 6
                    running_cost += travel_time_to_next * travel_cost + working_time * working_cost
                    current_time += get_distance(station, next_station) / truck_velocity + working_time
                    if current_time > 15:
                        break
            if result is None:
                result = np.array([[sat_profit, running_cost]])
            else:
                result = np.vstack((result, np.array([sat_profit, running_cost])))
        out["F"] = result

    @staticmethod
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

    @staticmethod
    def derivation_from_target_penalty_calculation(station, current_time, truck_inventory):
        rebalancing_amount = 0
        # print(station.demand)
        station_remaining_bike = min(max(station['bike_count'] - station['velocity'] * current_time, 0),
                                     station['max_capacity'])
        if station['demand'] > 0:
            rebalancing_amount = min(min(truck_inventory, station['demand']),
                                     station['max_capacity'] - station_remaining_bike)
            truck_inventory -= rebalancing_amount
        elif station['demand'] < 0:
            rebalancing_amount = min(min(-station['demand'], truck_capacity - truck_inventory), station['bike_count'])
            truck_inventory += rebalancing_amount
        return abs(abs(station['demand']) - abs(rebalancing_amount)), truck_inventory, abs(rebalancing_amount)
