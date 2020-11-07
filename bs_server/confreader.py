# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu
@license: Apache Licence 
@file: confreader.py
@time: 2020/10/16
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020
"""

import configparser
import os


def read_config(item, sub_item):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
    return config[item][sub_item]
