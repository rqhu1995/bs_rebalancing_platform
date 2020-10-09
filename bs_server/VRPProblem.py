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
from more_itertools import pairwise
from pymoo.model.problem import Problem

from .data import *


class BSRebalancing(Problem):

    def __init__(self):
        super().__init__(n_var=40, n_obj=3, n_constr=0, type_var=np.int)
        self.xl = np.zeros(self.n_var)
        self.xu = np.array([[42] * self.n_var])

    # 三个目标：满意度折算成本、调度量目标偏离惩罚、调度成本
    def _evaluate(self, x, out, *args, **kwargs):
        station_list = list(final_station_info.keys())
        result = None
        single_route = x.copy()
        for row in range(x.shape[0]):
            for col in range(x.shape[1]):
                single_route[row, col] = station_list[x[row, col]] if x[row, col] < 40 else 0
        for cnt in range(x.shape[0]):
            real_route = list(single_route[cnt, :])
            routes = [list(group) for k, group in groupby(real_route, lambda y: y == 0) if not k]
            objective_1 = 0
            objective_2 = 0
            objective_3 = 0
            for route in routes:
                current_time = 0
                truck_inventory = 0
                for station, next_station in pairwise(route + [route[0]]):
                    objective_1 -= 80 * self.satisfaction_calculation(station, current_time)
                    func_2 = self.derivation_from_target_penalty_calculation(station, truck_inventory)
                    objective_2 += 10 * func_2[0]
                    truck_inventory = func_2[1]
                    travel_time_to_next = distance_matrix[station, next_station] / truck_velocity
                    working_time = 1
                    objective_3 += travel_time_to_next * travel_cost + working_time * working_cost
                    current_time += distance_matrix[station, next_station] / truck_velocity + working_time
                    if current_time > 15:
                        break
            if result is None:
                result = np.array([[objective_1, objective_2, objective_3]])
            else:
                result = np.vstack((result, np.array([objective_1, objective_2, objective_3])))

        out["F"] = result

    @staticmethod
    def satisfaction_calculation(station, arriving_time):
        expected_time = station_info[station]['full_empty_time']
        if arriving_time <= expected_time:
            return 1
        elif expected_time < arriving_time < expected_time + reserved_time:
            return -1 / reserved_time * (arriving_time - expected_time - reserved_time)
        else:
            return 0

    @staticmethod
    def derivation_from_target_penalty_calculation(station, truck_inventory):
        station_demand = station_info[station]['demand']
        rebalancing_amount = 0
        max_capacity = station_info[station]['max_capacity']
        init_inventory = station_info[station]['init_inventory']
        if station_demand > 0:
            rebalancing_amount = min(min(truck_inventory, station_demand), max_capacity - init_inventory)
            truck_inventory -= rebalancing_amount
        elif station_demand < 0:
            rebalancing_amount = min(min(-station_demand, truck_capacity - truck_inventory), init_inventory)
            truck_inventory += rebalancing_amount
        return abs(abs(station_demand) - abs(rebalancing_amount)), truck_inventory
