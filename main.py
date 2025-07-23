import os
import subprocess

def run_script(script_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, script_name)
    print(f"\nRunning: {script_name}")
    subprocess.run(['python', script_path], check=True)

def main():
    print("Starting Full Knowledge Graph Pipeline")

    # 1. Extract raw Wikipedia content
    run_script('extract.py')

    # 2. Clean the raw text files
    run_script('clean.py')

    # 3. Extract subject-predicate-object triplets
    run_script('triplet_extract.py')

    # 4. Visualize graph from triplets
    run_script('graph_builder.py')

    # 5. Launch interactive querying tool
    run_script('query_graph.py')

    print("\nAll stages completed.")

if __name__ == '__main__':
    main()
