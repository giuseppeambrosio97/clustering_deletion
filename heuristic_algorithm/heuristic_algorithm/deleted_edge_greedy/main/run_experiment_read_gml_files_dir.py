"""
    This module can be used to run a the deleted_edge_greedy heuristic on all datasets contained
    in an input directory with the .gml format.

    How you can use it?
        - Make sure you are in the clustering_deletion/heuristic_algorithm directory.
        - Run the module with the appropriate parameters.
    e.g.
    python -u heuristic_algorithm/deleted_edge_greedy/main/run_experiment_read_gml_files_dir.py  \
              --dirname_in='/home/peppe/Scrivania/git_repo/clustering_deletion/data/exp/inputs/BA_instances_22m06d17/' \
             --filename_out='/home/giambrosio/per_git/clustering_deletion/data/exp/outputs/BA_instances_22m06d17.csv'
"""

import time

import fire
import networkx as nx
import pandas as pd
from heuristic_algorithm.deleted_edge_greedy.deleted_edge_greedy import deleted_edge_greedy
from heuristic_algorithm.utils.util_exp import read_dataset
from heuristic_algorithm.utils.check_solution import check_solution
import tqdm


def run_experiment_read_gml_dir(dirname_in: str, filename_out: str) -> None:
    """
        This function allows you to run the deleted_edge_greedy heuristic algorithm on all datasets 
        contained in the dirname_in directory and write the results of the execution to the 
        filename_out .csv file

    Args:
        dirname_in (str): path to a directory containing datasets in .gml format
        filename_out (str): path to a file in which the .csv file containing the 
                            results of the experiment will be written
    """    
    datasets = read_dataset(dirname_in)
    
    columns = [
        "Dataset name", 
        "n", 
        "m", 
        "Solution value", 
        "Time", 
        "isCorrect"
    ]
    df = pd.DataFrame(columns=columns, index=range(len(datasets)))

    for i, dataset in enumerate(tqdm.tqdm(datasets)):
        G = nx.read_gml(dataset, label="id")

        G_sol = G.copy()

        start_k = time.time()
        value = deleted_edge_greedy(G_sol)
        end_k = time.time() - start_k
        isCorrect = check_solution(G.copy(), G_sol, value)

        df.at[i, "Dataset name"] = dataset
        df.at[i, "n"] = len(G.nodes)
        df.at[i, "m"] = len(G.edges)
        df.at[i, "Solution value"] = value
        df.at[i, "Time"] = end_k
        df.at[i, "isCorrect"] = isCorrect

    df.to_csv(filename_out)
    

if __name__ == "__main__":
    fire.Fire(run_experiment_read_gml_dir)
