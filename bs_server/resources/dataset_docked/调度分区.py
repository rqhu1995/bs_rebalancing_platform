import math
import random
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
from sklearn.cluster import SpectralClustering

np.set_printoptions(threshold=np.inf)


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


for t in [60]:
    time_ind = math.floor(5 * 60 / t)
    # 调度量文件，两列，站点编号、调度量
    # 不需要调度的站点也需要放入文件中，调度量为0
    title = '动态调度量_08_'
    data = pd.read_csv(title[:-1] + '.csv', encoding='utf-8').iloc[:, 1].to_numpy()

    del_list = []
    for i in range(len(data)):
        if data[i] == 0:
            del_list.append(i)
    del_list = sorted(del_list, reverse=True)
    Hour = np.delete(data, del_list, axis=0)
    length = len(Hour)
    # print(Hour)
    print(length)

    # 站点坐标
    Vor_XY = pd.read_excel('Vor.xlsx').to_numpy()
    Vor_XY = np.delete(Vor_XY, del_list, axis=0)
    # print(Vor_XY)
    nodes = {}
    for i, point in enumerate(Vor_XY):
        nodes[str(int(point[0]))] = (point[1], point[2])

    G = nx.Graph()
    G.add_nodes_from(list(nodes.keys()))

    dis_max = 0
    dis_min = 999999
    flow_max = 0
    flow_min = 99999
    for i in range(length):
        for j in range(length):
            dis = haversine(nodes[str(int(Vor_XY[i][0]))], nodes[str(int(Vor_XY[j][0]))])
            if dis < 2:
                if dis > dis_max:
                    dis_max = dis
                if dis < dis_min:
                    dis_min = dis
            if Hour[i] * Hour[j] < 0:
                if abs(Hour[i] + Hour[j]) > flow_max:
                    flow_max = abs(Hour[i] + Hour[j])
                if abs(Hour[i] + Hour[j]) < flow_min:
                    flow_min = abs(Hour[i] + Hour[j])

    file = open(title + 'map_' + str(t) + '.csv', 'w')
    Weight = np.zeros((length, length))
    for i in range(length):
        for j in range(length):
            dis = haversine(nodes[str(int(Vor_XY[i][0]))], nodes[str(int(Vor_XY[j][0]))])
            if Hour[i] * Hour[j] < 0 and dis < 2:
                flow = abs(Hour[i] + Hour[j])

                dis = (dis - dis_min) / (dis_max - dis_min)
                flow = (flow - flow_min) / (flow_max - flow_min)
                # print(np.exp(-flow), dis)
                # dis = haversine(nodes[str(i + 1)], nodes[str(j + 1)])
                Weight[i][j] = np.exp(-flow) / dis
                G.add_weighted_edges_from([(str(int(Vor_XY[i][0])), str(int(Vor_XY[j][0])), Weight[i][j])])
                file.write(str(int(Vor_XY[i][0])) + ' ' + str(int(Vor_XY[j][0])) + ' ' + str(Weight[i][j]) + '\n')  #
                # G.add_weighted_edges_from([(str(i + 1), str(j + 1), Weight[i][j])])
            else:
                Weight[i][j] = 0
                # G.add_weighted_edges_from([(str(int(Vor_XY[i][0])), str(int(Vor_XY[j][0])), Weight[i][j])])
    np.save(title + 'Weight_' + str(t) + '.npy', Weight)
    file.close()
    file = open(title + 'infomap_' + str(t) + '.txt', 'w')
    file.close()

    # compute the best partition
    partition = community_louvain.best_partition(G)

    # print(partition.keys())
    # print(partition.values())
    # print(set(partition.values()))
    cluster = pd.Series(list(partition.values()))
    # print(cluster.value_counts())
    # print(community_louvain.modularity(partition, G))

    # draw the graph
    # color the nodes according to their partition
    # cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    # nx.draw_networkx_nodes(G, nodes, partition.keys(), node_size=10,
    #                        cmap=cmap, node_color=list(partition.values()))
    # nx.draw_networkx_edges(G, nodes, alpha=0.5)
    # plt.show()

    file = open('criterion.csv', 'a', encoding='utf-8')
    file.write(title + 'Louvain_' + str(t) + ',')
    area = pd.read_excel('Vor_attribute.xlsx').to_numpy()[:, -1]
    area = list(area)
    for ind in del_list:
        del area[ind]
    cluster = list(cluster)
    area_cluster = [0] * len(set(cluster))
    flow_cluster = [0] * len(set(cluster))
    # flow_cluster1 = [0] * len(set(cluster))
    center = np.array([[0.0, 0.0]] * len(set(cluster)))
    cluster_num = [0] * len(set(cluster))
    for i, point in enumerate(cluster):
        area_cluster[point] += area[i]
        flow_cluster[point] += data[i]
        # flow_cluster[point] += Rent[time_ind][i] + Return[time_ind][i]
        # flow_cluster1[point] += Rent[time_ind][i] - Return[time_ind][i]
        center[point][0] += nodes[str(int(Vor_XY[i][0]))][0]
        center[point][1] += nodes[str(int(Vor_XY[i][0]))][1]
        cluster_num[point] += 1
    for i in range(len(center)):
        center[i][0] /= cluster_num[i]
        center[i][1] /= cluster_num[i]
    dis_cluster = [0] * len(set(cluster))
    for i, point in enumerate(cluster):
        dis_cluster[point] += haversine(center[point], nodes[str(int(Vor_XY[i][0]))])
    # print(dis_cluster)
    print(flow_cluster)
    # print(np.average(flow_cluster))
    # print(area_cluster)
    # print(np.sqrt(np.average(np.array(area_cluster) ** 2)))
    # print(cluster_num)
    # print(np.var(cluster_num))

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
    cluster_Q = np.zeros((length, len(set(cluster))))
    for i in range(len(cluster_Q)):
        cluster_Q[i][cluster[i]] = 1
    modularity = Q(Weight, cluster_Q)
    # print(modularity)

    file.write(str(np.var(cluster_num)) + ',' + str(np.mean(dis_cluster)) + ',' + str(np.var(dis_cluster)) + ',')
    file.write(str(np.mean(area_cluster)) + ',' + str(np.var(area_cluster)) + ',')
    file.write(str(np.mean(np.abs(flow_cluster))) + ',' + str(np.var(np.abs(flow_cluster))) + ',')
    file.write(str(np.mean(leineisandu)) + ',' + str(np.mean(leijiansandu)) + ',')
    file.write(str(np.mean(zhandianxiangsixing)) + ',' + str(modularity) + '\n')
    # file.write(str(np.sum(np.abs(flow_cluster1))) + '\n')
    pd.DataFrame(center).to_csv('Center\\' + title + 'Louvain_center' + str(t) + '.csv', index=False)
    pd.DataFrame(
        np.concatenate((np.array(cluster, dtype=int).reshape((-1, 1)), Vor_XY), axis=1)).to_csv(
        title + 'Louvain_60_cluster' + str(t) + '.csv', index=False)
    # pd.DataFrame(Vor_XY).to_csv(title + 'Louvain_60_cluster_XY' + str(t) + '.csv', index=False)

    colors = ['red', 'green', 'blue', 'purple', 'yellow']
    for i in range(len((cluster))):
        d1 = nodes[str(int(Vor_XY[i][0]))]
        d2 = center[cluster[i]]
        c = cluster[i]
        plt.plot([d2[0], d1[0]], [d2[1], d1[1]], color=colors[c], linewidth=1)  #
    ax = plt.gca()
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    plt.xticks(fontsize=18)
    plt.xlabel('经度', fontsize=20)
    plt.yticks(fontsize=18)
    plt.ylabel('纬度', fontsize=20)
    plt.tight_layout()
    plt.savefig('Pic\\' + title + 'Louvian_' + str(t) + '.png', dpi=600)
    plt.show()
