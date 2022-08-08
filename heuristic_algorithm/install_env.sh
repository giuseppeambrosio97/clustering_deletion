#!/bin/bash
python -m pip install --upgrade pip
pip install virtualenv
python -m venv heuristic_alg_venv
source heuristic_alg_venv/bin/activate
pip install -e .