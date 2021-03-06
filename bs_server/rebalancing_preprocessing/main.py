# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu
@license: Apache Licence 
@file: main.py
@time: 2020/10/07
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020
"""
from flask import Flask, request
from flask.json import jsonify
from flask_cors import *

from bs_server.rebalancing_preprocessing.CustomJSONEncoder import CustomJSONEncoder
from bs_server.rebalancing_preprocessing.demand_calculation import *
from bs_server.rebalancing_preprocessing.station_info import StationInfo
from bs_server.rebalancing_preprocessing.topsis import priority_calculation

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.json_encoder = CustomJSONEncoder


def initialize_station_information():
    past_rent = np.array(
        [6, 4, 10, 0, 1, 20, 8, 9, 10, 26, 1, 6, 0, 4, 3, 18, 10, 4, 6, 17, 16, 2, 2, 3, 9, 3, 1, 5, 1, 1, 1, 2, 10, 6,
         1, 1, 3, 15, 3, 48, 2, 23, 5, 4, 9, 13, 7, 6, 10, 4, 3, 7, 11, 8, 7, 7, 5, 5, 0, 2, 5, 2, 11, 2, 13, 9, 6, 6,
         2, 23, 0, 7, 2, 7, 8, 4, 11, 4, 4, 11, 1, 11, 2, 1, 7, 2, 7, 12, 3, 3, 19, 8, 3, 3, 10, 14, 12, 5, 3, 16, 19,
         2, 3, 1, 4, 15, 2, 14, 2, 2, 7, 3, 6, 14, 2, 0, 4, 7, 14, 12, 10, 2, 3, 6, 18, 74, 1, 4, 1, 7, 5, 12, 11, 1,
         10, 3, 12, 2, 8, 6, 1, 11, 4, 5, 9, 20, 2, 9, 3, 0, 3, 4, 5, 9, 13, 12, 4, 11, 4, 2, 8, 6, 2, 1, 1, 2, 8, 6,
         12, 2, 20, 5, 3, 3, 1, 6, 2, 13, 7, 31, 5, 29, 0, 3, 15, 3, 2, 4, 12, 23, 8, 3, 22, 4, 14, 4, 3, 12, 5, 3, 10,
         4, 9, 4, 7, 3, 1, 6, 8, 21, 1, 6, 5, 2, 16, 22, 4, 5, 7, 12, 4, 28, 19, 3, 16, 9, 10, 2, 6, 9, 2, 21, 14, 7, 5,
         11, 0, 3, 10, 24, 5, 11, 10, 3, 3, 10, 1, 2, 5, 11, 27, 2, 3, 0, 6, 13, 10, 4, 1, 15, 8, 14, 9, 3, 18, 12, 8,
         0, 8, 4, 7, 15, 5, 16, 7, 15, 2, 5, 4, 2, 17, 3, 2, 3, 14, 10, 5, 7, 8, 3, 7, 6, 2, 18, 6, 10, 2, 0, 0, 6])
    past_return = np.array(
        [6, 15, 8, 1, 3, 3, 9, 9, 6, 27, 6, 4, 12, 2, 3, 10, 22, 2, 2, 2, 31, 4, 3, 1, 2, 12, 7, 7, 0, 1, 5, 4, 3, 16,
         11, 3, 14, 4, 5, 39, 6, 20, 7, 1, 10, 5, 11, 3, 3, 3, 6, 12, 5, 7, 7, 1, 5, 10, 1, 2, 8, 11, 6, 4, 7, 12, 17,
         12, 1, 10, 2, 8, 7, 3, 9, 6, 3, 1, 2, 1, 1, 24, 9, 5, 7, 3, 6, 5, 7, 7, 10, 7, 4, 5, 8, 9, 9, 12, 7, 5, 27, 5,
         5, 1, 6, 2, 10, 8, 7, 2, 6, 2, 9, 2, 4, 0, 2, 8, 3, 8, 11, 3, 6, 3, 4, 35, 4, 3, 8, 9, 8, 6, 5, 3, 12, 4, 5, 5,
         12, 7, 0, 4, 3, 10, 6, 22, 7, 7, 2, 0, 1, 2, 11, 3, 8, 1, 5, 16, 1, 1, 13, 4, 8, 11, 10, 6, 18, 2, 7, 3, 22,
         12, 8, 14, 4, 2, 7, 9, 4, 35, 7, 12, 5, 3, 12, 6, 8, 9, 6, 3, 5, 6, 10, 4, 3, 5, 7, 5, 10, 7, 14, 3, 11, 5, 10,
         4, 15, 7, 10, 15, 9, 12, 5, 8, 8, 24, 7, 15, 2, 4, 13, 25, 9, 5, 1, 3, 13, 7, 1, 16, 5, 11, 8, 2, 7, 11, 5, 6,
         8, 17, 4, 8, 2, 2, 11, 4, 4, 8, 5, 18, 15, 1, 4, 9, 9, 8, 5, 3, 14, 6, 8, 3, 11, 5, 8, 5, 4, 3, 5, 5, 3, 14,
         10, 10, 5, 3, 2, 2, 4, 2, 7, 12, 2, 4, 24, 10, 3, 4, 5, 3, 7, 4, 3, 15, 14, 14, 1, 1, 3, 4])
    pred_rent = np.array(
        [70, 10, 49, 6, 21, 106, 31, 42, 19, 85, 7, 52, 13, 16, 48, 30, 21, 44, 37, 77, 42, 17, 53, 29, 55, 66, 16, 28,
         7, 14, 6, 62, 20, 27, 22, 5, 9, 24, 10, 131, 3, 40, 52, 11, 20, 36, 10, 58, 29, 13, 39, 19, 48, 34, 67, 9, 26,
         25, 2, 17, 25, 19, 46, 7, 30, 42, 16, 24, 10, 140, 2, 29, 19, 41, 53, 13, 38, 14, 5, 45, 13, 25, 8, 18, 76, 8,
         34, 40, 36, 33, 69, 43, 14, 32, 39, 47, 47, 13, 5, 46, 83, 15, 9, 9, 13, 75, 7, 42, 27, 39, 38, 46, 26, 70, 11,
         5, 31, 46, 63, 74, 132, 5, 26, 67, 43, 187, 5, 9, 15, 48, 20, 48, 31, 29, 97, 16, 31, 10, 38, 27, 8, 18, 8, 26,
         42, 66, 13, 29, 2, 1, 20, 36, 5, 26, 45, 64, 14, 28, 54, 48, 53, 78, 13, 14, 19, 30, 22, 16, 81, 16, 79, 19,
         26, 22, 11, 29, 10, 45, 27, 94, 17, 102, 32, 9, 37, 49, 14, 5, 86, 90, 69, 11, 94, 48, 107, 28, 26, 59, 15, 30,
         16, 27, 38, 9, 37, 20, 16, 14, 30, 97, 9, 26, 32, 20, 82, 61, 15, 16, 48, 46, 12, 94, 95, 4, 79, 14, 51, 7, 29,
         54, 4, 29, 57, 15, 8, 35, 30, 8, 33, 89, 19, 56, 62, 15, 41, 37, 17, 6, 16, 33, 173, 20, 26, 7, 21, 25, 44, 45,
         16, 43, 22, 95, 19, 15, 56, 86, 62, 6, 38, 14, 31, 57, 14, 57, 59, 72, 5, 45, 4, 40, 60, 20, 78, 9, 45, 27, 53,
         43, 61, 55, 88, 80, 3, 53, 27, 53, 23, 25, 2, 19])
    pred_return = np.array(
        [26, 32, 36, 12, 8, 51, 18, 132, 42, 130, 9, 53, 24, 15, 26, 22, 66, 27, 20, 12, 87, 19, 17, 13, 26, 46, 32, 35,
         3, 9, 7, 29, 21, 44, 36, 8, 41, 60, 24, 193, 23, 114, 43, 7, 32, 49, 26, 29, 25, 23, 32, 55, 26, 41, 38, 15,
         24, 37, 3, 17, 36, 26, 38, 17, 31, 59, 35, 45, 11, 32, 10, 27, 30, 36, 44, 23, 18, 22, 4, 14, 10, 64, 21, 28,
         25, 11, 55, 32, 39, 14, 20, 46, 4, 28, 36, 40, 79, 29, 17, 19, 190, 33, 26, 10, 18, 31, 27, 31, 31, 16, 48, 37,
         48, 42, 30, 2, 15, 39, 37, 46, 58, 10, 13, 38, 31, 229, 3, 24, 31, 36, 33, 25, 24, 28, 48, 6, 23, 20, 53, 40,
         19, 24, 6, 59, 65, 144, 27, 27, 3, 0, 20, 27, 12, 20, 81, 50, 18, 52, 28, 5, 44, 19, 30, 29, 39, 22, 55, 11,
         31, 22, 163, 33, 19, 34, 16, 25, 42, 33, 22, 169, 40, 34, 35, 7, 61, 10, 34, 22, 31, 38, 39, 38, 60, 31, 53,
         27, 27, 55, 16, 31, 41, 7, 51, 20, 52, 24, 49, 19, 38, 66, 38, 60, 40, 27, 22, 96, 20, 54, 26, 44, 33, 118, 20,
         18, 43, 21, 33, 19, 35, 67, 10, 72, 48, 19, 34, 149, 17, 9, 36, 86, 33, 73, 45, 20, 42, 38, 17, 19, 26, 46, 43,
         15, 25, 26, 28, 38, 21, 24, 19, 22, 35, 39, 29, 11, 78, 28, 36, 9, 37, 34, 27, 82, 35, 95, 38, 28, 14, 35, 8,
         6, 37, 46, 21, 20, 99, 72, 21, 72, 38, 20, 28, 50, 5, 121, 55, 87, 11, 15, 9, 18])
    velocity = calculate_rent_return_velocity(
        past_rent=past_rent,
        past_return=past_return,
        pred_rent=pred_rent,
        pred_return=pred_return
    )
    station_dict = {}
    for i in range(300):
        station = StationInfo(i)
        calculate_full_empty_time(station, velocity, 60)
        calculate_warning_time(station, velocity, 60)
        calculate_demand(station, 60, velocity)
        station.ratio = round(initial_bike[i] / max_capacity[i], 2)
        station.latest_time = station.full_empty_time + 5
        station_dict[i] = station.__dict__
        station.velocity = round(velocity[i], 2)
    return station_dict


# 分区接口
@app.route('/clustering', methods=['POST'])
@cross_origin()
def update_cluster():
    station_data = request.get_json()
    cluster_result = {0: 0, 1: 1, 2: 2, 3: 1, 4: 0, 5: 2, 6: 1, 9: 1, 10: 3, 11: 3, 12: 1, 13: 2, 14: 2, 15: 0, 16: 1,
                      17: 2, 18: 1, 19: 0, 20: 0, 21: 3, 22: 2, 23: 1, 24: 1, 26: 2, 28: 0, 30: 3, 32: 2, 33: 3, 34: 0,
                      35: 1, 36: 1, 37: 3, 38: 2, 39: 0, 40: 2, 43: 1, 44: 0, 45: 1, 46: 0, 47: 0, 48: 2, 51: 3, 52: 1,
                      55: 2, 56: 2, 57: 1, 59: 2, 61: 1, 62: 0, 63: 2, 64: 0, 65: 1, 66: 0, 67: 1, 68: 1, 69: 2, 70: 2,
                      72: 1, 73: 1, 75: 2, 76: 3, 79: 0, 80: 1, 81: 3, 82: 0, 83: 2, 84: 0, 87: 2, 88: 3, 89: 2, 90: 3,
                      92: 3, 94: 3, 95: 2, 97: 2, 98: 2, 99: 1, 100: 0, 101: 0, 105: 1, 106: 1, 107: 1, 109: 3, 110: 1,
                      113: 0, 114: 1, 115: 2, 116: 1, 117: 2, 118: 3, 119: 0, 120: 3, 122: 2, 123: 0, 124: 1, 125: 1,
                      126: 2, 128: 3, 130: 1, 131: 3, 132: 1, 133: 1, 134: 3, 135: 2, 136: 1, 137: 2, 138: 0, 139: 2,
                      141: 3, 142: 2, 143: 0, 144: 1, 146: 0, 147: 1, 148: 3, 149: 1, 150: 0, 152: 2, 153: 2, 154: 0,
                      155: 3, 156: 3, 157: 1, 158: 0, 159: 1, 160: 3, 161: 0, 162: 2, 163: 1, 164: 1, 165: 1, 166: 0,
                      167: 2, 168: 1, 169: 0, 170: 2, 171: 0, 172: 2, 173: 0, 174: 3, 175: 1, 176: 1, 177: 2, 178: 0,
                      179: 1, 180: 2, 181: 0, 182: 3, 183: 2, 184: 1, 185: 0, 186: 1, 187: 0, 188: 2, 189: 0, 190: 3,
                      191: 0, 192: 1, 194: 0, 195: 2, 196: 2, 197: 3, 198: 0, 199: 1, 200: 1, 201: 1, 202: 0, 203: 2,
                      204: 0, 205: 3, 206: 0, 207: 2, 209: 1, 210: 0, 211: 0, 213: 0, 214: 2, 215: 3, 217: 0, 218: 0,
                      219: 3, 220: 1, 221: 1, 222: 2, 223: 0, 224: 3, 225: 3, 226: 0, 227: 1, 228: 2, 230: 2, 231: 1,
                      232: 2, 233: 2, 234: 1, 235: 0, 237: 2, 238: 1, 239: 1, 240: 0, 241: 2, 242: 3, 244: 0, 245: 0,
                      247: 1, 248: 0, 249: 3, 250: 0, 253: 3, 254: 2, 256: 1, 257: 0, 258: 1, 259: 1, 261: 3, 262: 3,
                      263: 2, 264: 3, 265: 1, 266: 1, 267: 2, 268: 3, 269: 1, 271: 0, 272: 1, 274: 0, 275: 0, 276: 1,
                      277: 1, 278: 1, 279: 1, 280: 0, 281: 1, 282: 1, 283: 2, 284: 2, 285: 2, 286: 2, 288: 3, 289: 0,
                      290: 3, 291: 0, 292: 2, 293: 1, 294: 0, 295: 3, 296: 2, 298: 2}
    for station_info in station_data:
        if station_info['station_id'] in cluster_result.keys():
            station_info['cluster'] = cluster_result[station_info['station_id']] + 1
        else:
            station_info['cluster'] = "不参与调度"
    return jsonify(station_data)


# 重要度计算接口
@app.route('/priority', methods=['POST'])
@cross_origin()
def update_priority():
    station_data = request.get_json()
    selected_cluster = station_data[0]['cluster']
    calculate_distance(station_data, selected_cluster)
    topsis_indicator = pd.DataFrame(station_data)[['station_id', 'full_empty_time', 'demand', 'distance']]
    priority = priority_calculation(topsis_indicator)
    pri_dict = priority.set_index('ID').T.to_dict('dict')
    for station in station_data:
        station['priority'] = round(pri_dict[station['station_id']]['e'], 2)
    return jsonify(station_data)


@app.route('/station_info', methods=['GET'])
@cross_origin()
def get_station_info():
    station_info = initialize_station_information()
    obj = jsonify(station_info)
    return obj


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=5000, debug=None)
