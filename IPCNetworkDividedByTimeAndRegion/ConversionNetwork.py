import pandas as pd
import networkx as nx
import numpy as np
import os

def create_network_from_ipc(df):
    # Prepare the graph
    G = nx.Graph()
    for index, row in df.iterrows():
        ipc_list = [i.strip() for i in row['IPC'].split('|') if i.strip()]
        for node in ipc_list:
            if node not in G:
                G.add_node(node, weight=0)
            G.nodes[node]['weight'] += 1
        for i in range(len(ipc_list)):
            for j in range(i + 1, len(ipc_list)):
                if G.has_edge(ipc_list[i], ipc_list[j]):
                    G[ipc_list[i]][ipc_list[j]]['weight'] += 1
                else:
                    G.add_edge(ipc_list[i], ipc_list[j], weight=1)
    return G

def calculate_network_properties(G):
    clustering_coeff = nx.average_clustering(G)
    largest_cc = max(nx.connected_components(G), key=len)
    subgraph = G.subgraph(largest_cc)
    if nx.is_connected(subgraph):
        avg_path_len = nx.average_shortest_path_length(subgraph)
    else:
        avg_path_len = float('nan')  # if the subgraph is not connected
    
    # Community detection for modularity
    communities = nx.algorithms.community.greedy_modularity_communities(G)
    modularity = nx.algorithms.community.modularity(G, communities)

    return clustering_coeff, modularity, avg_path_len

def process_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            time_country = filename[:-4]
            df = pd.read_csv(os.path.join(input_dir, filename))
            df = df[df['IPC'] != '0']  # Removing rows where IPC value is '0'
            G = create_network_from_ipc(df)
            clustering_coeff, modularity, avg_path_len = calculate_network_properties(G)
            
            num_nodes = G.number_of_nodes()
            num_edges = G.number_of_edges()
            
            # Create file name based on the network properties
            output_filename = f"{time_country}_{num_nodes}_{num_edges}_{clustering_coeff:.2f}_{modularity:.2f}_{avg_path_len:.2f}.gexf"
            nx.write_gexf(G, os.path.join(output_dir, output_filename))

# Example usage
input_directory = './IPCNetworkDividedByTimeAndRegion/IPCDividedDataset'
output_directory = './IPCNetworkDividedByTimeAndRegion/IPCDividedNetwork'
process_files(input_directory, output_directory)
