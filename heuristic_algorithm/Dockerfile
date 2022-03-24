FROM python:3.9.5

WORKDIR /application/heuristic_algorithm

COPY ./requirements.txt .
COPY ./setup.py .
COPY ./heuristic_algorithm ./heuristic_algorithm

RUN pip install -e .

ENTRYPOINT ["python", "heuristic_algorithm/deleted_edge_greedy/main/main-esempio-tesi.py"]