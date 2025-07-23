import csv
import os
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt

def filter_triplets_by_entity_frequency(triplets, min_freq=3):
    counter = Counter()
    for subj, pred, obj in triplets:
        counter[subj] += 1
        counter[obj] += 1
    return [(s, p, o) for s, p, o in triplets if counter[s] >= min_freq and counter[o] >= min_freq]

def build_graph(triplets):
    G = nx.DiGraph()
    for subj, pred, obj in triplets:
        G.add_node(subj)
        G.add_node(obj)
        G.add_edge(subj, obj, label=pred)
    return G

def visualize_graph(G, output_path):
    plt.figure(figsize=(20, 12))
    pos = nx.spring_layout(G, k=0.9, iterations=100)  # more spread
    nx.draw(
        G, pos, with_labels=True, node_color='skyblue', 
        node_size=2500, edge_color='gray', 
        font_size=9, font_weight='bold', arrows=True
    )
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_color='red', font_size=8
    )
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.show()

def load_triplets(filepath):
    triplets = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) == 3:
                triplets.append(tuple(row))
    return triplets

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    triplet_path = os.path.normpath(os.path.join(base_dir, '..', 'data', 'triplets.csv'))
    output_img = os.path.normpath(os.path.join(base_dir, '..', 'data', 'kg_output.png'))

    triplets = load_triplets(triplet_path)
    filtered_triplets = filter_triplets_by_entity_frequency(triplets, min_freq=3)

    G = build_graph(filtered_triplets)
    visualize_graph(G, output_img)

if __name__ == '__main__':
    main()
