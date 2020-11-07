# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu
@license: Apache Licence 
@file: moead_run.py
@time: 2020/10/03
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020
"""
import datetime
import json
from multiprocessing.pool import ThreadPool

import numpy as np
import pandas as pd
from numpyencoder import NumpyEncoder
from pymoo.algorithms.moead import MOEAD
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation, get_termination
from pymoo.factory import get_visualization, get_reference_directions
from pymoo.optimize import minimize

from bs_server.confreader import read_config as cfg
from bs_server.data import station_info
from bs_server.rebalancing_preprocessing.routedistributionrepair import RouteDistributionRepair
from bs_server.rebalancing_routing.VRPProblem import BSRebalancing
from bs_server.result_evaluation.evaluate import evaluate

# client = Client()
# the number of threads to be used
n_threads = 32

# initialize the pool
pool = ThreadPool(n_threads)


def calculate_spacing(result_F):
    fitness_obj = np.unique(result_F, axis=0)
    d_i = np.zeros((len(fitness_obj),))
    for i in range(len(fitness_obj)):
        for j in range(len(fitness_obj)):
            cur = np.sum(np.abs(fitness_obj[j] - fitness_obj[i]))
            if d_i[i] > cur:
                d_i[i] = cur
    avg_di = np.average(d_i)
    std = np.std(d_i)
    return std


def moead_run(i):
    problem = BSRebalancing(parallelization=('starmap', pool.starmap))
    ref_dir = get_reference_directions("das-dennis", 2, n_partitions=99)
    seed = i
    algorithm = MOEAD(
        ref_dir,
        pop_size=100,
        sampling=get_sampling("perm_random"),
        n_neighbors=20,
        crossover=get_crossover("perm_erx"),
        mutation=get_mutation("perm_inv"),
        decomposition="tchebi",
        prob_neighbor_mating=0.7,
        seed=seed,
        eliminate_duplicates=True
    )

    algorithm.repair = RouteDistributionRepair(ref_dir)

    # termination = get_termination("time", "00:00:30")
    termination = get_termination("n_gen", 250)

    res = minimize(problem, algorithm, termination, seed=seed, save_history=True)

    get_visualization("scatter").add(res.F).show()
    route_index = np.unique(res.X, axis=0)
    # calculate_spacing(res.F)
    final_result = res.F
    station_list = list(station_info.keys())[4:]
    result_solution = np.zeros(route_index.shape)
    for row in range(route_index.shape[0]):
        for col in range(route_index.shape[1]):
            result_solution[row, col] = station_list[route_index[row, col]] if route_index[row, col] < int(
                cfg('station_info', 'station_count')) else -1

    # n_evals = []  # corresponding number of function evaluations\
    # F = []  # the objective space values in each generation
    # cv = []  # constraint violation in each generation
    #
    # # iterate over the deepcopies of algorithms
    # for algorithm in res.history:
    #     # store the number of function evaluations
    #     n_evals.append(algorithm.evaluator.n_eval)
    #
    #     # retrieve the optimum from the algorithm
    #     opt = algorithm.opt
    #
    #     # store the least contraint violation in this generation
    #     cv.append(opt.get("CV").min())
    #
    #     # filter out only the feasible and append
    #     feas = np.where(opt.get("feasible"))[0]
    #     _F = opt.get("F")[feas]
    #     F.append(_F)
    #
    # ref_point = np.array([-150, 200])
    #
    # # create the performance indicator object with reference point
    # metric = Hypervolume(ref_point=ref_point, normalize=False)
    #
    # # calculate for each generation the HV metric
    # hv_res = [metric.calc(f) for f in F]
    return result_solution, final_result, res.exec_time


np.set_printoptions(threshold=np.inf)
result = []


for i in range(20):
    res = moead_run(i)
    for idx, route in enumerate(res[0]):
        route_eval = evaluate(route.astype(int))
        if route_eval[:4] not in result:
            result.append(route_eval)
        routing_report = route_eval[4]
        file = open("battle_pri_upgrade/routes/exp_result_" + datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + str(idx) + ".json",
                    encoding='utf-8', mode='w+')
        json.dump(routing_report, file, cls=NumpyEncoder)
        file.close()

    pd.DataFrame(result).to_csv("battle_pri_upgrade/exp_result_" + datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + str(i) + ".csv")
    print(str(res[2]))
