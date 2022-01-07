#!/bin/sh
conda create --prefix ./env
cd $(pwd)/env
conda install -file requirements.txt
pip install -e .