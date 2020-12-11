# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu
@license: Apache Licence 
@file: moead_run.py
@time: 2020/10/07
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020
"""
import pandas as pd
from flask import Flask, request
from flask.json import jsonify
from flask_cors import *

from bs_server.confreader import read_config as cfg
from bs_server.data import rebalanced_info, station_list, visited
from bs_server.rebalancing_preprocessing.CustomJSONEncoder import CustomJSONEncoder
from bs_server.rebalancing_preprocessing.clustering import cluster_louvain
from bs_server.rebalancing_preprocessing.demand_calculation import *
from bs_server.rebalancing_preprocessing.infomap_comD import cluster_infomap
from bs_server.rebalancing_preprocessing.station_info import Station
from bs_server.rebalancing_preprocessing.topsis import priority_calculation

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.json_encoder = CustomJSONEncoder
station_count = int(cfg('station_info', 'station_count'))
# 初始化数据库连接:x
engine = create_engine('mysql+mysqldb://root:95930908@localhost:3306/bikeshare_docked')
# 创建DBSession类型:
Session = sessionmaker(bind=engine)
current_stage = int(cfg('meta_info', 'current_stage'))


def update_current_station_status(station_id_list):
    session = Session()
    if current_stage == 0:
        bike_count_init = pd.read_csv(
            '/Users/hurunqiu/project/bs_rebalancing_platform/bs_server/resources/dataset_docked/station_info_overall.csv',
            header=0, usecols=[0, 4]).set_index('id').T.to_dict()

        for idx, station_id in enumerate(station_id_list):
            station = session.query(Station).filter_by(id=station_id[0]).first()
            station.visited = False
            station.bike_count = bike_count_init[station.id]['bike_count']
        session.commit()
        return
    for route in rebalanced_info['routes']:
        for idx, station_id in enumerate(route['station_list']):
            station = session.query(Station).filter_by(id=station_id).first()
            station.visited = True
            station.bike_count -= route['actual_allocation'][idx]
    for station_id in station_id_list:
        station = session.query(Station).filter_by(id=station_id[0]).first()
        past_rent_list = [station.past_rent_01, station.past_rent_02, station.past_rent_03, station.past_rent_04]
        past_return_list = [station.past_return_01, station.past_return_02, station.past_return_03,
                            station.past_return_04]

        station.bike_count -= (past_rent_list[current_stage - 1] - past_return_list[current_stage - 1])
        station.bike_count = max(0, min(station.bike_count, station.max_capacity))
    session.commit()


def update_station_information(update):
    session = Session()
    station_id_list = session.query(Station.id).all()
    if update:
        update_current_station_status(station_id_list)
    for station_id in station_id_list:
        session = Session()
        station = session.query(Station).filter_by(id=station_id[0]).first()
        calculate_rent_return_velocity(station, current_stage, 15, 60 - current_stage * 15)
        calculate_full_empty_time(station, station.velocity, 60 - current_stage * 15)
        calculate_demand(station, 60 - current_stage * 15, station.velocity)
        station.ratio = round(station.bike_count / station.max_capacity, 2)
        session.commit()


# 分区接口
@app.route('/clustering', methods=['POST'])
@cross_origin()
def update_cluster():
    station_data = get_all_station_info().get_json()
    cluster_method = request.data.decode('UTF-8')
    cluster_df = pd.DataFrame(station_data)[['id', 'demand']]
    cluster_result = None
    if cluster_method == 'Louvain':
        cluster_result = cluster_louvain(cluster_df)
    elif cluster_method == 'Infomap':
        cluster_result = cluster_infomap(cluster_df)
    else:
        return None
    # print(cluster_result)
    session = Session()
    for i in range(1, 301):
        station = session.query(Station).filter_by(id=i).first()
        if i in cluster_result.keys():
            station.cluster = cluster_result[i]
        else:
            station.cluster = -1
        print(str(i) + " settled!")
    session.commit()
    """
    for station in station_data:
        if station.visited:
            station['cluster'] = 1
        else:
            station['cluster'] = "不参与调度"
    """
    station_data = get_all_station_info().get_json()
    return jsonify(station_data)


# 重要度计算接口
@app.route('/priority', methods=['POST'])
@cross_origin()
def update_priority():
    session = Session()
    session.query(Station).filter(Station.priority != 0).update({'priority': None})
    session.commit()
    station_data = get_station_info(False).get_json()
    selected_cluster = 1
    calculate_distance(station_data, selected_cluster)
    station_data = get_station_info(False).get_json()
    print(station_data)
    topsis_indicator = pd.DataFrame(station_data)[['id', 'full_empty_time', 'demand', 'key_distance']]
    print(topsis_indicator)
    topsis_indicator = topsis_indicator[(topsis_indicator.demand != 0) & topsis_indicator['id'].isin(station_list) &
    (~topsis_indicator['id'].isin(visited))]
    print(topsis_indicator)
    priority = priority_calculation(topsis_indicator)
    # print(priority)
    pri_dict = priority.set_index('ID').T.to_dict('dict')
    for station in station_data:
        station_obj = session.query(Station).filter_by(id=station['id']).first()
        if station['id'] in pri_dict.keys():
            station['priority'] = round(pri_dict[station['id']]['e'], 2)
            station_obj.priority = station['priority']
        else:
            station_obj.priority = -1
    # print(sorted(station_data, key=lambda i: i['priority'], reverse=True)[:station_count])
    session.commit()
    return jsonify(station_data)


@app.route('/station_info', methods=['GET'])
@cross_origin()
def get_station_info(update=True):
    obj = get_all_station_info(update)
    return obj


def get_all_station_info(update=True):
    update_station_information(update)
    session = Session()
    res = []
    result = session.query(Station).all()
    for record in result:
        res.append(record.to_json())
    obj = jsonify(res)
    return obj


if __name__ == '__main__':
    app.run()
