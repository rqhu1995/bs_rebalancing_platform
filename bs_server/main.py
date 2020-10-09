# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu
@license: Apache Licence 
@file: main.py
@time: 2020/10/03
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020
"""

import pandas as pd
import numpy as np
from pymoo.algorithms.moead import MOEAD
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation, get_termination
from pymoo.factory import get_visualization, get_reference_directions
from pymoo.optimize import minimize

from bs_server.VRPProblem import BSRebalancing

problem = BSRebalancing()
ref_dir = get_reference_directions("das-dennis", 3, n_partitions=14)
algorithm = MOEAD(
    ref_dir,
    pop_size=120,
    sampling=get_sampling("perm_random"),
    n_neighbors=15,
    crossover=get_crossover("perm_erx"),
    mutation=get_mutation("perm_inv"),
    decomposition="pbi",
    prob_neighbor_mating=0.7,
    seed=1,
    eliminate_duplicates=True
)

termination = get_termination("n_gen", 200)

res = minimize(problem, algorithm, termination, seed=1, save_history=True)

get_visualization("scatter").add(res.F).show()
print(np.unique(res.X, axis=0).shape)
