import math
import random
import numpy as np
import pandas as pd
from jgraph import *
from infomap import Infomap
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font_cn = FontProperties(fname='/Users/hurunqiu/Library/Fonts/SimSun.ttf')
font_en = FontProperties(fname='/System/Library/Fonts/Supplemental/Times New Roman.ttf')
# plt.rcParams.update({
#     "text.usetex": False,
#     "font.family": 'times new roman',
#     "font.weight":'light'}
# )

def haversine(vec1, vec2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    if len(vec1) == 1:
        vec1 = vec1[0]
    if len(vec2) == 1:
        vec2 = vec2[0]
    lon1, lat1 = vec1
    lon2, lat2 = vec2
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r  # * 1000


def Q(array, cluster):
    # 总边数
    m = sum(sum(array)) / 2
    k1 = np.sum(array, axis=1)
    k2 = k1.reshape(k1.shape[0], 1)
    # 节点度数积
    k1k2 = k1 * k2
    # 任意两点连接边数的期望值
    Eij = k1k2 / (2 * m)
    # 节点v和w的实际边数与随机网络下边数期望之差
    B = array - Eij
    # 获取节点、社区矩阵
    node_cluster = np.dot(cluster, np.transpose(cluster))
    results = np.dot(B, node_cluster)
    # 求和
    sum_results = np.trace(results)
    # 模块度计算
    Q = sum_results / (2 * m)
    # print("Q:", Q)
    return Q

def cluster_infomap(cluster_df):
    im = Infomap()
    im.read_file(
        "/Users/hurunqiu/project/bs_rebalancing_platform/bs_server/rebalancing_preprocessing/动态调度量_08_map_60.csv")
    idx = 0
    im.run('--clu --ftree')
    title = '动态调度量_08_'
    with open(title + 'infomap_' + str(60) + '.txt', 'a', encoding='utf-8') as f:  # 数据中每行三个数，点一，点二，权值
        for node in im.nodes:
            for i in im.modules:
                if i[0] == node.node_id:
                    idx = i[1]
                    break
            f.write(str(node.node_id) + ' ' + str(idx) + ' ' + str(node.flow) + "\n")
    f.close()

    for t in [60]:  # 15, 30, 60, 120
        time_ind = math.floor(5 * 60 / t)
        with open(title + 'infomap_' + str(t) + '.txt') as f:  # 数据中每行三个数，点一，点二，权值
            data = f.readlines()
        node = []
        for i in data:
            line = i.strip().split(' ')
            if int(line[0]) not in node:
                node.append(int(line[0]))
        node = sorted(node)

        full_nodes = [i + 1 for i in range(300)]
        del_list = list(set(full_nodes).difference(set(node)))
        del_list = sorted(del_list, reverse=True)
        for i in range(len(del_list)):
            del_list[i] -= 1
        cluster = [0] * len(node)
        for i in data:
            line = i.strip().split(' ')
            cluster[node.index(int(line[0]))] = int(line[1])
        # print(cluster)
        Vor_XY = pd.read_excel('Vor.xlsx').to_numpy()
        Vor_XY = np.delete(Vor_XY, del_list, axis=0)

        # Rent = np.load('Dockless_Rent' + str(t) + '.npy')
        # Rent = np.sum(Rent, axis=2).reshape(-1, 300)
        # Return = np.load('Dockless_Return' + str(t) + '.npy')
        # Return = np.sum(Return, axis=1).reshape(-1, 300)
        # Diff = Rent - Return
        # Hour = Diff[time_ind]

        # Hour = pd.read_csv(title[:-1] + '.csv', encoding='utf-8').iloc[:, 1].to_numpy()
        Hour = cluster_df.iloc[:, 1].to_numpy()

        nodes = {}
        for i, point in enumerate(Vor_XY):
            nodes[str(int(point[0]))] = (point[1], point[2])

        area = pd.read_excel('Vor_attribute.xlsx').to_numpy()[:, -1]
        area = list(area)
        for ind in del_list:
            del area[ind]
        # print(len(area))
        cluster = list(cluster)

        center = np.array([[0.0, 0.0]] * len(set(cluster)))
        cluster_num = [0] * len(set(cluster))
        for i, point in enumerate(cluster):
            center[point - 1][0] += nodes[str(int(Vor_XY[i][0]))][0]
            center[point - 1][1] += nodes[str(int(Vor_XY[i][0]))][1]
            cluster_num[point - 1] += 1
        for i in range(len(center)):
            center[i][0] /= cluster_num[i]
            center[i][1] /= cluster_num[i]

        for i, point in enumerate(cluster):
            dis = haversine(center[point - 1], nodes[str(int(Vor_XY[i][0]))])
            if dis >= 1.9:
                dis_min = 999
                num_min = 0
                for j, cent in enumerate(center):
                    d = haversine(cent, nodes[str(int(Vor_XY[i][0]))])
                    if d < dis_min:
                        dis_min = d
                        num_min = j
                cluster[i] = num_min + 1

        file = open('criterion.csv', 'a', encoding='utf-8')
        file.write(title + 'Infomap_' + str(t) + ',')

        area_cluster = [0] * len(set(cluster))
        flow_cluster = [0] * len(set(cluster))
        # flow_cluster1 = [0] * len(set(cluster))
        center = np.array([[0.0, 0.0]] * len(set(cluster)))
        cluster_num = [0] * len(set(cluster))
        for i, point in enumerate(cluster):
            area_cluster[point - 1] += area[i]
            flow_cluster[point - 1] += Hour[i]
            # flow_cluster[point - 1] += Rent[time_ind][i] + Return[time_ind][i]
            # flow_cluster1[point - 1] += Rent[time_ind][i] - Return[time_ind][i]
            center[point - 1][0] += nodes[str(int(Vor_XY[i][0]))][0]
            center[point - 1][1] += nodes[str(int(Vor_XY[i][0]))][1]
            cluster_num[point - 1] += 1
        for i in range(len(center)):
            center[i][0] /= cluster_num[i]
            center[i][1] /= cluster_num[i]
        dis_cluster = [0] * len(set(cluster))
        for i, point in enumerate(cluster):
            dis_cluster[point - 1] += haversine(center[point - 1], nodes[str(int(Vor_XY[i][0]))])
        print(cluster_num)
        # 各类坐标的字典
        cluster_dict = {}
        for c in set(cluster):
            for i in range(len(cluster)):
                if cluster[i] == c:
                    if c not in cluster_dict:
                        cluster_dict[c] = [Vor_XY[i]]
                    else:
                        cluster_dict[c].append(Vor_XY[i])
        # 类内散度
        leineisandu = [0] * len(set(cluster))
        for n, key in enumerate(cluster_dict.keys()):
            for i in range(len(cluster_dict[key])):
                for j in range(i + 1, len(cluster_dict[key])):
                    leineisandu[n] += haversine(cluster_dict[key][i][1:], cluster_dict[key][j][1:])
            leineisandu[n] = np.sqrt(2 * leineisandu[n] / cluster_num[n])
        # print(leineisandu)
        # 类间散度
        leijiansandu = []
        keys = list(cluster_dict.keys())
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                value = 0
                for m in cluster_dict[keys[i]]:
                    for n in cluster_dict[keys[j]]:
                        value += haversine(m[1:], n[1:])
                num1 = len(cluster_dict[keys[i]])
                num2 = len(cluster_dict[keys[j]])
                value = np.sqrt((num1 + num2) * value / (num1 * num2))
                leijiansandu.append(value)
        # print(leijiansandu)
        # 站点数量相似性测度
        zhandianxiangsixing = [0] * len(set(cluster))
        avg = np.around(np.average(cluster_num) + 0.5)
        for i in range(len(zhandianxiangsixing)):
            zhandianxiangsixing[i] = np.abs(cluster_num[i] - avg)
        # print(zhandianxiangsixing)
        # 模块儿度
        cluster_Q = np.zeros((len(cluster), len(set(cluster))))
        Weight = np.load(title + 'Weight_' + str(t) + '.npy')
        for i in range(len(cluster_Q)):
            cluster_Q[i][cluster[i] - 1] = 1
        modularity = Q(Weight, cluster_Q)
        # print(modularity)

        # print(flow_cluster)
        # print(np.average(flow_cluster))
        # print(area_cluster)
        # print(np.sqrt(np.average(np.array(area_cluster) ** 2)))
        # print(cluster_num)
        # print(np.average(cluster_num))
        # file.write(str(np.var(cluster_num)) + ',' + str(np.mean(dis_cluster)) + ',' + str(np.var(dis_cluster)) + ',')
        # file.write(str(np.mean(area_cluster)) + ',' + str(np.var(area_cluster)) + ',')
        file.write(str(np.mean(np.abs(flow_cluster))) + ',')
        file.write(str(np.mean(leineisandu)) + ',' + str(np.mean(leijiansandu)) + ',')
        file.write(str(np.mean(zhandianxiangsixing)) + ',' + str(modularity) + '\n')
        file.close()
        # file.write(str(np.sum(np.abs(flow_cluster1))) + '\n')
        pd.DataFrame(center).to_csv(title + 'Infomap_center' + str(t) + '.csv', index=False)
        result = pd.DataFrame(
            np.concatenate((np.array(cluster, dtype=int).reshape((-1, 1)), Vor_XY), axis=1))
        result.to_csv(
            title + 'Infomap_60_cluster' + str(t) + '.csv', index=False)

        colors = ['red', 'green', 'blue', 'purple']
        # r = lambda: random.randint(0, 255)
        # for index in range(len(center)):
        #     colors.append(('#%02X%02X%02X' % (r(), r(), r())))
        # plt.figure(figsize=(8, 6))
        for i in range(len((cluster))):
            d1 = nodes[str(int(Vor_XY[i][0]))]
            d2 = center[cluster[i] - 1]
            c = cluster[i] - 1
            plt.plot([d2[0], d1[0]], [d2[1], d1[1]], color=colors[c], linewidth=1)  #
        # plt.show()
        ax = plt.gca()
        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        plt.xticks(fontsize=28, fontproperties=font_en)
        plt.xlabel('经度', fontsize=28, fontproperties=font_cn)
        plt.yticks(fontsize=28, fontproperties=font_en)
        plt.ylabel('纬度', fontsize=28, fontproperties=font_cn)
        plt.tight_layout()
        plt.savefig(title + 'Infomap_' + str(t) + '.png', dpi=600)
        plt.show()
        result = result.set_index(1).T.to_dict('dict')
        final_cluster = {}
        for item in result.keys():
            final_cluster[int(item)] = int(result[item][0])
        return final_cluster