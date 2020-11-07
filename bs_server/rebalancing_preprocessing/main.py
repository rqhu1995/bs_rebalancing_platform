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
from flask import Flask, request
from flask.json import jsonify
from flask_cors import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs_server.rebalancing_preprocessing.clustering import cluster_louvain
from bs_server.rebalancing_preprocessing.infomap_comD import cluster_infomap

from bs_server.confreader import read_config as cfg
from bs_server.rebalancing_preprocessing.CustomJSONEncoder import CustomJSONEncoder
from bs_server.rebalancing_preprocessing.demand_calculation import *
from bs_server.rebalancing_preprocessing.station_info import Station
from bs_server.rebalancing_preprocessing.topsis import priority_calculation

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.json_encoder = CustomJSONEncoder
station_count = int(cfg('station_info', 'station_count'))
# 初始化数据库连接:
engine = create_engine('mysql+mysqldb://root:95930908@localhost:3306/bikeshare')
# 创建DBSession类型:
Session = sessionmaker(bind=engine)
current_stage = 0

all_stations = [125, 105, 265, 90, 16, 259, 176, 159, 239, 124, 256, 168, 9, 175, 1, 279, 186, 72, 73, 43, 227, 6, 106,
                24, 149, 99, 116, 201, 23, 45, 209, 107, 277, 67, 192, 282, 57, 110, 132, 3, 242, 61, 165, 178, 52, 200,
                65, 157, 18, 199, 147, 136, 276, 133]


def update_station_information():
    for i in range(1, station_count + 1):
        session = Session()
        station = session.query(Station).filter_by(id=i).first()
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
    station_data = get_all_station_info()
    selected_cluster = 1
    calculate_distance(station_data, selected_cluster)
    topsis_indicator = pd.DataFrame(station_data)[['station_id', 'full_empty_time', 'demand', 'distance']]
    priority = priority_calculation(topsis_indicator)
    pri_dict = priority.set_index('ID').T.to_dict('dict')
    for station in station_data:
        station['priority'] = round(pri_dict[station['station_id']]['e'], 2)
    print(sorted(station_data, key=lambda i: i['priority'], reverse=True)[:station_count])
    return jsonify(station_data)


@app.route('/station_info', methods=['GET'])
@cross_origin()
def get_station_info():
    obj = get_all_station_info()
    return obj


def get_all_station_info():
    update_station_information()
    session = Session()
    res = []
    result = session.query(Station).all()
    for record in result:
        res.append(record.to_json())
    obj = jsonify(res)
    return obj


if __name__ == '__main__':
    app.run()
