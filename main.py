import numpy as np
import pandas as pd
import networkx as nx
import time
import random
from collections import defaultdict
from tqdm import *
import argparse
import matplotlib.pyplot as plt

from algorithm.optimal_minimized import find_optimal_alpha
from algorithm.dijkstra_shortest import dijkstra

def build_network(edges_df, od_df):

    # 初始化有向图
    G = nx.DiGraph()
    edges = [(row['source'], row['target'], {'t0': row['t0'], 'C': row['capacity']}) for index, row in edges_df.iterrows()]
    G.add_edges_from(edges)
    od_pairs = {(row['origin'], row['destination']): row['demand'] for index, row in od_df.iterrows()}

    # 必须进行非零初始化，用于加速迭代
    for u, v in G.edges():
        # G[u][v]['V'] = 0
        G[u][v]['V'] = random.randint(0, G[u][v]['C']-1)
    
    return G, od_pairs


def all_none_tmp(edges, od_groups):

    # 全有全无法生成辅助流量
    edge_to_idx = {(u, v): i for i, (u, v) in enumerate(edges)}
    y = np.zeros(len(edges))
    for o in od_groups:
        try:
            paths = dijkstra(G, o, weight='t')
            for d, q in od_groups[o]:
                if d in paths:
                    path = paths[d]
                    for i in range(len(path)-1):
                        u, v = path[i], path[i+1]
                        y[edge_to_idx[(u, v)]] += q
        except nx.NetworkXNoPath:
            continue

    return y


def FW_allocation(G, od_pairs, max_iter, tol):

    # 预处理边列表和属性数组
    edges = list(G.edges())
    t0_arr = np.array([G[u][v]['t0'] for u, v in edges])
    C_arr = np.array([G[u][v]['C'] for u, v in edges])
    od_groups = defaultdict(list)
    for (o, d), q in od_pairs.items():
        od_groups[o].append((d, q))

    # 计算当前阻抗
    for iter in tqdm(range(max_iter)):
        time.sleep(0.05)
        for u, v in G.edges():
            V = G[u][v]['V']
            C = G[u][v]['C']
            G[u][v]['t'] = G[u][v]['t0'] / (1 - V/C) if V < C else 1e6
        y = all_none_tmp(edges, od_groups)

        # 计算当前流量数组和方向向量
        V_current = np.array([G[u][v]['V'] for u, v in edges])
        d = y - V_current
        
        # 定义向量化目标函数
        def obj(alpha):
            new_V = V_current + alpha * d
            if np.any(new_V >= C_arr):
                return np.inf
            else:
                return np.sum(t0_arr / (1-new_V/C_arr))
        
        # 优化步长
        alpha = find_optimal_alpha(obj, bounds=(0, 1))
        if alpha < tol:
            print(f'Converged after {iter+1} iterations.')
            break
        # 更新流量
        V_new = V_current + alpha * d
        for i, (u, v) in enumerate(edges):
            G[u][v]['V'] = V_new[i]

    return G


def visulize_network(G, pos_df):

    pos_df = pd.read_csv(r'.\data\map.csv')
    pos = {row['node']: (row['x'], row['y']) for index, row in pos_df.iterrows()}

    edge_labels_1 = {(u, v): '{:.1f}'.format(G[u][v]['V']) for u, v in G.edges()}
    edge_labels_2 = {}
    ls = list(edge_labels_1.keys())
    for (u, v) in ls:
        if (v, u) in edge_labels_1:
            edge_labels_1.pop((v, u))
            ls.remove((v, u))
            edge_labels_2[(v, u)] = '{:.1f}'.format(G[v][u]['V'])

    plt.figure(figsize=(6, 6))
    nx.draw_networkx_edges(
        G, pos, 
        edgelist=edge_labels_1, 
        width=2, 
        edge_color='red', 
        arrowsize=20, 
        connectionstyle='arc3,rad=0.1')
    nx.draw_networkx_edges(
        G, pos, 
        edgelist=edge_labels_2, 
        width=2, edge_color='blue', 
        arrowsize=20, 
        connectionstyle='arc3,rad=0.1')
    nx.draw_networkx_edge_labels(
        G, pos, 
        edge_labels=edge_labels_1, 
        font_size=9,
        label_pos=0.3,
        rotate=0,
        verticalalignment='top')
    nx.draw_networkx_edge_labels(
        G, pos, 
        edge_labels=edge_labels_2, 
        font_size=9,
        label_pos=0.3,
        rotate=0,
        verticalalignment='bottom')

    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='lightblue', edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=12)

    plt.title('Optimized Traffic Flow Allocation', fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--edges', type=str, default='data/edges.csv', help='The directory of csv that describe the nodes and edges of digraph')
    parser.add_argument('--od', type=str, default='data/od_pairs.csv', help='The directory of csv that discribe OD pairs')
    parser.add_argument('--pos', type=str, default='data/map.csv', help='The directory of csv that describes the shape of digraph')
    parser.add_argument('--max_iter', type=int, default=10000, help='The maximum number of iterations')
    parser.add_argument('--tol', type=int, default=1e-8, help='The minimum alpha tolerance')
    args = parser.parse_args()

    edges_df = pd.read_csv(args.edges)
    od_df = pd.read_csv(args.od)
    pos_df = pd.read_csv(args.pos)
    max_iter = args.max_iter
    tol = args.tol

    G, od_pairs = build_network(edges_df, od_df)
    G_assigned = FW_allocation(G, od_pairs, max_iter, tol)
    visulize_network(G_assigned, pos_df)
