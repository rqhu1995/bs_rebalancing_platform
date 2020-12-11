# -*- coding:utf-8 _*-
""" 
@author:Runqiu Hu, Mingjia He
@license: Apache Licence 
@file: topsis.py 
@time: 2020/10/08
@contact: hurunqiu@live.com
@project: bikeshare rebalancing

* Cooperating with Dr. Matt in 2020
"""

import math

import numpy as np
import pandas


def indicator_direction_unify(indicator_df):
    # 同向化处理
    df_cpy = indicator_df[['full_empty_time', 'demand', 'key_distance']]
    df_cpy.loc[:, 'demand'] = df_cpy.loc[:, 'demand'].map(lambda x: abs(x))
    df_cpy.loc[:, 'key_distance'] = df_cpy.loc[:, 'key_distance'].map(lambda x: float(df_cpy.loc[:, 'key_distance'].max() - x))
    df_cpy.loc[:, 'full_empty_time'] = df_cpy.loc[:, 'full_empty_time'].map(
        lambda x: float(df_cpy.loc[:, 'full_empty_time'].max() - x))
    df_cpy = pandas.DataFrame(df_cpy.values.T, index=df_cpy.columns, columns=df_cpy.index)
    # print(df_cpy)
    return df_cpy


def normalize(data):
    denominator = np.power(np.sum(pow(data, 2), axis=1), 0.5)
    for i in range(0, denominator.size):
        for j in range(0, data[i].size):
            data[i, j] = data[i, j] / denominator[i]  # 套用矩阵标准化的公式
    # print(data)
    return data


def calculate_score(answer2):
    # 熵权法计算权重
    data = answer2
    sumzb = np.sum(data, axis=1)
    data[0] = data[0] / sumzb[0]
    data[1] = data[1] / sumzb[1]
    data[2] = data[2] / sumzb[2]
    a = data * 1.0
    a[np.where(data == 0)] = 0.0001
    # print(a[1])
    # print(np.log(a[1]))
    e = (-1.0 / np.log(len(data[0]))) * np.sum(data * np.log(a), axis=1)
    # print(e)
    w = (1 - e) / np.sum(1 - e)

    answer2[0] = answer2[0] * w[0]
    answer2[1] = answer2[1] * w[1]
    answer2[2] = answer2[2] * w[2]

    list_max = np.array(
        [np.max(answer2[0, :]), np.max(answer2[1, :]), np.max(answer2[2, :])])
    list_min = np.array(
        [np.min(answer2[0, :]), np.min(answer2[1, :]), np.min(answer2[2, :])])

    max_list = []  # 存放第i个评价对象与最大值的距离
    min_list = []  # 存放第i个评价对象与最小值的距离
    answer_list = []  # 存放评价对象的未归一化得分
    for k in range(0, np.size(answer2, axis=1)):  # 遍历每一列数据
        max_sum = 0
        min_sum = 0
        for q in range(0, 3):  # 有四个指标
            max_sum += np.power(answer2[q, k] - list_max[q], 2)  # 按每一列计算Di+
            min_sum += np.power(answer2[q, k] - list_min[q], 2)  # 按每一列计算Di-
        max_list.append(pow(max_sum, 0.5))
        min_list.append(pow(min_sum, 0.5))
        answer_list.append(min_list[k] / (min_list[k] + max_list[k]))  # 套用计算得分的公式 Si = (Di-) / ((Di+) +(Di-))
        max_sum = 0
        min_sum = 0
    # print(max_list)
    # print(min_list)
    answer = np.array(answer_list)  # 得分归一化
    # print(answer)
    return answer_list


def priority_calculation(indicator_df):
    indicator = indicator_direction_unify(indicator_df)
    df1 = np.array(indicator)  # 将list转换为numpy数组
    answer3 = normalize(df1)  # 数组正向化
    answer4 = calculate_score(answer3)  # 标准化处理去钢
    data = pandas.DataFrame(answer4)  # 计算得分
    data['rank'] = data.rank(ascending=False)
    indicator_df.reset_index(drop=True, inplace=True)
    data['ID'] = indicator_df['id']
    a = data['rank'].rank(ascending=True)
    data['e'] = a.values
    data['e'] = data['e'].map(lambda x: float(10 * math.exp(1 - x / len(data["rank"]))))  # 提计算参数,一
    data.to_csv("topsis_res.csv")
    return data
