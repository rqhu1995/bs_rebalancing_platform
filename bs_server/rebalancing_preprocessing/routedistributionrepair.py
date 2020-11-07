# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu
@license: Apache Licence 
@file: routedistributionrepair.py
@time: 2020/10/10
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020
"""
import time
from itertools import groupby

import numpy as np
from pymoo.model.repair import Repair

from confreader import read_config as cfg
from data import station_info
from result_evaluation.evaluate import evaluate

station_count = int(cfg('station_info', 'station_count'))
truck_count = int(cfg('station_info', 'truck_count'))
consider_priority = bool(cfg('meta_info', 'priority_considered'))


def get_index_by_priority(num):
    for item in station_info.keys():
        if station_info[item]['priority'] == num:
            return list(station_info.keys()).index(item)


def fix_priority_dist(routes):
    priority_rng = []
    priority = []
    for idx, route in enumerate(routes):
        pri = []
        station_list = list(station_info.keys())
        for station in route:
            pri.append(station_info[station_list[station]]['priority'])
        priority_rng.append(np.max(pri) - np.min(pri))
        priority.append(pri)
    rng = sorted(priority_rng, reverse=False)
    idx1, idx2 = priority_rng.index(rng[0]), priority_rng.index(rng[1])
    tmp = sorted(priority[idx1] + priority[idx2], reverse=True)
    max_1, max_2, min_1, min_2 = tmp[0],\
                                 tmp[1],\
                                 tmp[len(tmp)-2],\
                                 tmp[len(tmp)-1]
    if len({max_1, max_2, min_1, min_2})!=4 :
        return routes
    pri_idx = []
    # print([max_1, max_2, min_1, min_2])

    for num in [max_1, max_2, min_1, min_2]:
        pri_idx.append(get_index_by_priority(num))
    # print([max_1, max_2, min_1, min_2])
    # print(pri_idx)

    for idx in pri_idx:
        if idx in routes[idx1]:
            routes[idx1].remove(idx)
        if idx in routes[idx2]:
            routes[idx2].remove(idx)
    routes[idx1].insert(0, pri_idx[0])
    routes[idx1].append(pri_idx[2])
    routes[idx2].insert(0, pri_idx[1])
    routes[idx2].append(pri_idx[3])
    return routes

class RouteDistributionRepair(Repair):
    def __init__(self, ref_dir):
        self.ref_dir = ref_dir

    def _do(self, problem, pop, **kwargs):
        # sub_idx = kwargs['subproblem_index']
        # the routing information population (each row one individual)
        population = pop.get("X")
        # print(population.shape)
        # the packing plan for i
        z = population
        # zres = []
        # for zidx, z in enumerate(zp):
        # find all the trucks in the population, insert them as averagely as possible
        stations = z[z < station_count]
        split = np.array_split(stations, truck_count)
        result = []
        for idx, chunk in enumerate(split):
            if idx != len(split) - 1:
                chunk = np.append(chunk, station_count + idx)
            result = result + list(chunk)
        z = np.asarray(result)
        z = np.asarray(self.priority_repair(z))

        # set the design variables for the population
        pop.set("X", z)
        return pop

    def priority_repair(self, solution):
        new_solution = None
        counter = 0
        while counter < 10 and self.is_dominated_by(new_solution, solution):
            counter += 1
            routes = [list(group) for k, group in groupby(solution, lambda y: y >= station_count) if not k]
            new_solution = []
            routes = fix_priority_dist(routes)
            for idx, route in enumerate(routes):
                tmp = route.copy()
                selected = self.roulette_wheel(route)
                # print(route)
                selected = selected['origin_index']
                # print(list(station_info.keys())[selected])
                tmp.remove(selected)
                new_sol = [selected] + list(tmp)
                new_solution += list(new_sol) + [station_count + idx]
                # print("origin:" + str(route))
                # print("new:   " + str(new_sol))
        if new_solution is None or self.is_dominated_by(new_solution[:-1], solution):
            return solution
        else:
            return new_solution[:-1]

    @staticmethod
    def roulette_wheel(solution):
        population = []
        station_list = list(station_info.keys())
        for station in solution:
            population.append({
                'origin_index': station,
                'station_id': station_list[station],
                'priority': station_info[station_list[station]]['priority']
            })
        maximum = sum([c['priority'] for c in population])
        selection_probs = [c['priority'] / maximum for c in population]
        k = population[np.random.choice(len(population), p=selection_probs)]
        # print(k['station_id'])
        return k

    @staticmethod
    def is_dominated_by(new_sol, solution):
        if new_sol is None or solution is None:
            return True
        new_sol_map = []
        old_sol_map = []
        for station in new_sol:
            new_sol_map.append(list(station_info.keys())[station] if station < station_count else -1)
        for station in solution:
            old_sol_map.append(list(station_info.keys())[station] if station < station_count else -1)
        eval_new = evaluate(new_sol_map)
        eval_old = evaluate(old_sol_map)
        return eval_new[0] >= eval_old[0] or eval_new[2] <= eval_old[2]
