# CLUSTERING DELETION HEURISTIC ALGORITHM

## Run on pc ##

create the virtual environment (you can use the script install_env.sh to do it).
```console
python -m pip install --upgrade pip
pip install virtualenv
python -m venv heuristic_alg_venv
source heuristic_alg_venv/bin/activate
pip install -e .
```


## Run with docker ##

```console
docker build -t heuristic_algorithm .
docker run heuristic_algorithm
```
