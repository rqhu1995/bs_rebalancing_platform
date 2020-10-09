# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu
@license: Apache Licence 
@file: station_info.py
@time: 2020/10/08
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020
"""
import json

from numpyencoder import NumpyEncoder


class StationInfo:
    """basic information of a station"""

    def __init__(self,
                 station_id,
                 demand=None,
                 ratio=None,
                 diversity=None,
                 full_empty_time=None,
                 warning_time=None,
                 latest_time=None,
                 cluster=None,
                 priority=None,
                 velocity=None,
                 key_distance=None):
        """Constructor for StationInfo"""
        self.station_id = station_id
        self.demand = demand
        self.ratio = ratio
        self.diversity = diversity
        self.full_empty_time = full_empty_time
        self.warning_time = warning_time
        self.latest_time = latest_time
        self.cluster = cluster
        self.priority = priority
        self.key_distance = None
