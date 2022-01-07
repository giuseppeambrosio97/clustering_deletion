#!/bin/sh
conda create --prefix ./env
conda activate $(pwd)/env
conda install --file requirements.txt
pip install -e .