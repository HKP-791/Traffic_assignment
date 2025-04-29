import heapq
from collections import defaultdict

def dijkstra(G, start_node, weight='t'):
    # 初始化数据结构
    shortest_paths = {start_node: [start_node]}
    distances = {node: float('inf') for node in G.nodes()}
    distances[start_node] = 0
    
    # 优先队列 (distance, node)
    heap = []
    heapq.heappush(heap, (0, start_node))
    
    # 前驱节点记录
    predecessors = defaultdict(list)
    
    while heap:
        current_dist, current_node = heapq.heappop(heap)
        
        # 如果找到更短路径则跳过旧记录
        if current_dist > distances[current_node]:
            continue
            
        # 遍历出边（针对有向图）
        for neighbor in G.successors(current_node):
            edge_data = G[current_node][neighbor]
            w = edge_data[weight]  # 使用't'作为权重
            new_dist = current_dist + w
            
            # 发现更短路径
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = [current_node]
                heapq.heappush(heap, (new_dist, neighbor))
                
            # 相同距离的不同路径
            elif new_dist == distances[neighbor]:
                predecessors[neighbor].append(current_node)
    
    # 构建路径字典（只保留一条最短路径）
    paths = {}
    for node in G.nodes():
        if distances[node] == float('inf'):
            continue
        path = []
        current = node
        while current != start_node:
            path.insert(0, current)
            current = predecessors[current][0]  # 取第一条路径
        path.insert(0, start_node)
        paths[node] = path
        
    return paths

if __name__ == '__main__':
    # for test
    # G = nx.Graph()
    # G.add_edge('A', 'B', t=5)
    # G.add_edge('A', 'C', t=3)
    # G.add_edge('B', 'C', t=2)
    # G.add_edge('B', 'D', t=4)
    # G.add_edge('C','D', t=6)
    pass