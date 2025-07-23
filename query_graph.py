import os
import csv
import networkx as nx

def load_triplets(filepath):
    triplets = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) == 3:
                triplets.append(tuple(row))
    return triplets

def build_graph(triplets):
    G = nx.DiGraph()
    for subj, pred, obj in triplets:
        G.add_edge(subj, obj, label=pred)
    return G

def get_connections(G, entity):
    connections = list(G[entity].items())
    return [(entity, attr['label'], target) for target, attr in connections]

def save_connections_to_file(conns, entity, path):
    filename = f"{entity}_connections.txt"
    filepath = os.path.join(path, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        for s, p, o in conns:
            file.write(f"{s} --[{p}]--> {o}\n")
    print(f"Saved to: {filepath}")

def find_paths(G, source, target, max_depth=3):
    try:
        return list(nx.all_simple_paths(G, source=source, target=target, cutoff=max_depth))
    except nx.NetworkXNoPath:
        return []

def list_all_predicates(G):
    return set(nx.get_edge_attributes(G, 'label').values())

def rank_entities_by_degree(G, top_k=10):
    degrees = G.degree()
    sorted_degrees = sorted(degrees, key=lambda x: x[1], reverse=True)
    return sorted_degrees[:top_k]

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    triplet_path = os.path.normpath(os.path.join(base_dir, '..', 'data', 'triplets.csv'))
    output_dir = os.path.normpath(os.path.join(base_dir, '..', 'data'))

    triplets = load_triplets(triplet_path)
    G = build_graph(triplets)

    print("=== Knowledge Graph Query Tool ===")
    while True:
        print("\nOptions:")
        print("1. Search connections of an entity")
        print("2. Find all paths between two entities")
        print("3. List all predicates")
        print("4. Rank top entities by centrality")
        print("5. Exit")

        choice = input("Enter choice [1-5]: ")

        if choice == '1':
            entity = input("Enter entity name: ")
            if entity in G:
                conns = get_connections(G, entity)
                for s, p, o in conns:
                    print(f"{s} --[{p}]--> {o}")
                export = input("Export to file? (y/n): ").strip().lower()
                if export == 'y':
                    save_connections_to_file(conns, entity, output_dir)
            else:
                print("Entity not found.")
        
        elif choice == '2':
            src = input("Enter source entity: ")
            tgt = input("Enter target entity: ")
            paths = find_paths(G, src, tgt)
            if paths:
                for path in paths:
                    print(" -> ".join(path))
            else:
                print("No path found.")
        
        elif choice == '3':
            preds = list_all_predicates(G)
            print("Predicates:")
            for p in preds:
                print(f"- {p}")

        elif choice == '4':
            print("Top entities by centrality (degree):")
            top_entities = rank_entities_by_degree(G)
            for i, (node, score) in enumerate(top_entities, start=1):
                print(f"{i}. {node} (degree: {score})")
        
        elif choice == '5':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()
