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

from geopy.distance import geodesic
from more_itertools import pairwise
from pymoo.model.problem import Problem

from confreader import read_config as cfg
from data import *

station_count = int(cfg('station_info', 'station_count'))
truck_count = int(cfg('station_info', 'truck_count'))


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
        # if len(x.shape) < 2:
        #     x = x.reshape((1, -1))
        # 站点按照重要度排序的下标列表
        station_list = list(station_info.keys())[4:]
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
            for idx, route in enumerate(routes):
                # 当前时间
                route.insert(0, list(station_info.keys())[idx])
                current_time = 0
                # 车场抵达第一站
                center_to_first = geodesic((lat_lon[route[0]][1], lat_lon[route[0]][0]), center).km / truck_velocity
                current_time += center_to_first
                running_cost += center_to_first * travel_cost
                truck_inventory = 60
                for station, next_station in pairwise(route + [route[0]]):
                    func_2 = self.derivation_from_target_penalty_calculation(station, truck_inventory)
                    sat_profit -= 1 * self.satisfaction_calculation(station, current_time, func_2[2])
                    truck_inventory = func_2[1]
                    travel_time_to_next = distance_matrix[station, next_station] / truck_velocity
                    working_time = func_2[2] * 1 / 6
                    running_cost += travel_time_to_next * travel_cost + working_time * working_cost
                    current_time += distance_matrix[station, next_station] / truck_velocity + working_time
                    if current_time > 15:
                        break
            if result is None:
                result = np.array([[sat_profit, running_cost]])
            else:
                result = np.vstack((result, np.array([sat_profit, running_cost])))

        out["F"] = result

    @staticmethod
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

    @staticmethod
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
