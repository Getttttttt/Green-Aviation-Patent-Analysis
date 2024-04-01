import pandas as pd
import networkx as nx
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_network():
    df = pd.read_csv('./Dataset/IPCInfo.csv')
    df['IPC'] = df['IPC'].apply(lambda x: [i.strip() for i in x.split('|')])
    G = nx.Graph()
    for ipc_list in df['IPC']:
        for node in ipc_list:
            if node not in G:
                G.add_node(node, weight=0)
            G.nodes[node]['weight'] += 1
        for i in range(len(ipc_list)):
            for j in range(i+1, len(ipc_list)):
                if G.has_edge(ipc_list[i], ipc_list[j]):
                    G[ipc_list[i]][ipc_list[j]]['weight'] += 1
                else:
                    G.add_edge(ipc_list[i], ipc_list[j], weight=1)

    if not os.path.exists(f'./IPCNetwork'):
        os.makedirs(f'./IPCNetwork')
    nx.write_pajek(G, f'./IPCNetwork/IPCNetwork.net')

    # 输出网络的节点数和边数
    print("节点数:", G.number_of_nodes())
    print("边数:", G.number_of_edges())
    
    return G

def calculate_centrality(G):
    centrality_measures = {
        'degree_centrality': nx.degree_centrality(G),
        'betweenness_centrality': nx.betweenness_centrality(G),
        'eigenvector_centrality': nx.eigenvector_centrality(G, max_iter=100000, tol=1e-06),
        'pagerank': nx.pagerank(G),
        'core_number': nx.core_number(G),
        'closeness_centrality': nx.closeness_centrality(G),
    }

    # 将重要性指标的字典转换为DataFrame
    df_centrality = pd.DataFrame(centrality_measures)

    # 将索引（节点名称）添加为一列
    df_centrality['node'] = df_centrality.index

    # 重新排列列的顺序
    cols = ['node'] + [col for col in df_centrality.columns if col != 'node']
    df_centrality = df_centrality[cols]

    # 保存为CSV文件
    df_centrality.to_csv(f'./IPCNetwork/node_centrality_measures.csv', index=False)

def rich_club(G):
    # Calculate the rich-club coefficient for the network
    rich_club_dict_small = nx.rich_club_coefficient(G, normalized=True, Q=100)
    degrees_small, coefficients_small = zip(*rich_club_dict_small.items())

    # Plot the rich-club coefficient for the smaller network
    plt.figure(figsize=(10, 6))
    plt.plot(degrees_small, coefficients_small, 'b-', lw=2)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Degree', fontsize=14)
    plt.ylabel('Rich-Club Coefficient', fontsize=14)
    plt.title('Rich-Club Coefficient vs Degree', fontsize=16)
    plt.grid(True, which="both", ls="--")
    plt.savefig('./IPCNetwork/Images/rich_club.png')
    plt.close()
    
def degree_to_degree_correlation(G):
    # Calculate the average neighbor degree for each node in the smaller network
    avg_neighbor_deg_small = nx.average_neighbor_degree(G)

    # Calculate the degree of each node in the smaller network
    node_degrees = dict(G.degree())

    # Prepare data for plotting
    degrees = np.array(list(node_degrees.values()))
    avg_neighbors_deg = np.array(list(avg_neighbor_deg_small.values()))

    # Calculate degree assortativity coefficient of the smaller network
    assortativity_coefficient = nx.degree_assortativity_coefficient(G)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.scatter(degrees, avg_neighbors_deg, alpha=0.5, edgecolor='none')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Node Degree', fontsize=14)
    plt.ylabel('Average Neighbor Degree', fontsize=14)
    plt.title('Node Degree vs. Average Neighbor Degree', fontsize=16)
    plt.grid(True, which="both", ls="--")
    print(assortativity_coefficient)
    plt.savefig('./IPCNetwork/Images/node_degree.png')
    plt.close()


if __name__ == '__main__':
    G = load_network()

    calculate_centrality(G)

    rich_club(G)

    degree_to_degree_correlation(G)

