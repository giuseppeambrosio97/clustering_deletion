# Clustering Deletion

This repository contains the implementation of exact and heuristic algorithms for the Clustering Deletion problem as described in our paper "Exact and Heuristic Solution Approaches for the Cluster Deletion Problem on General Graphs" published in the Networks journal ([DOI: 10.1002/net.22267](https://onlinelibrary.wiley.com/doi/pdf/10.1002/net.22267)).

## About the Problem

Clustering Deletion is an NP-hard graph clustering problem with applications in computational biology, bioinformatics, and wireless sensor networks. The objective is to find the smallest subset of edges to be removed from a network to produce a cluster graph (a disjoint union of cliques), which is equivalent to determining the largest subset of edges to be preserved.

In the graph-theoretic approach to clustering, a similarity graph is created where nodes represent items to be clustered, and two nodes are connected by an edge if the similarity between the related items is higher than a predefined threshold. The Clustering Deletion problem aims to perform the minimum number of edge deletions to obtain a cluster graph, prioritizing homogeneity over separation of clusters.

## Repository Structure

- **data/**: Contains instances of real and generated graphs used in our experiments.
  - Includes both artificial instances and benchmark biological networks
  
- **exact_algorithm/**: Implementation of exact algorithms for the Clustering Deletion problem.
  - Utilizes integer linear programming models
  - Includes preprocessing techniques to reduce instance size
  
- **heuristic_algorithm/**: Implementation of heuristic algorithms providing approximate solutions.
  - Features an approach based on edge contraction operations
  - Faster solutions for large-scale instances

## Installation

### Exact Algorithm

Dependencies are managed through Python's standard library. No additional installation steps are required.

### Heuristic Algorithm

#### Option 1: Using Virtual Environment

```bash
python -m pip install --upgrade pip
pip install virtualenv
python -m venv heuristic_alg_venv
source heuristic_alg_venv/bin/activate
cd heuristic_algorithm
pip install -e .
```

#### Option 2: Using Docker

```bash
cd heuristic_algorithm
docker build -t heuristic_algorithm .
docker run heuristic_algorithm
```

## Usage

### Exact Algorithm

Navigate to the exact_algorithm directory and run:

```bash
python CCModel.py [arguments]
```

### Heuristic Algorithm

After installing dependencies:

```bash
cd heuristic_algorithm
python -m heuristic_algorithm [arguments]
```

Refer to the specific README files in each directory for detailed usage instructions and available command-line arguments.

## Experiments

The algorithms were evaluated on:

- Artificially generated instances
- Benchmark biological networks

Performance metrics include:

- Solution quality (minimum number of edges to delete)
- Computation time
- Scalability with graph size

## Cite Us

If you use our code or reference our work in your research, please cite our paper:

```
@article{ambrosio2025exact,
  title = {Exact and Heuristic Solution Approaches for the Cluster Deletion Problem on General Graphs},
  author = {Ambrosio, Giuseppe and Cerulli, Raffaele and Serra, Domenico and Sorgente, Carmine and Vaccaro, Ugo},
  journal = {Networks},
  volume = {},
  number = {},
  pages = {1--17},
  year = {2025},
  publisher = {Wiley Periodicals LLC},
  doi = {10.1002/net.22267}
}
```

## License

This software is released under the Creative Commons Attribution License, which permits use, distribution, and reproduction in any medium, provided the original work is properly cited.

## Contributors

- Giuseppe Ambrosio - Department of Computer Science, University of Salerno, Fisciano, Salerno, Italy
- Raffaele Cerulli - Department of Mathematics, University of Salerno, Fisciano, Salerno, Italy
- Domenico Serra - Department of Mathematics, University of Salerno, Fisciano, Salerno, Italy
- Carmine Sorgente - Department of Mathematics, University of Salerno, Fisciano, Salerno, Italy
- Ugo Vaccaro - Department of Computer Science, University of Salerno, Fisciano, Salerno, Italy

## Acknowledgments

[Research was conducted at the University of Salerno, Italy]
